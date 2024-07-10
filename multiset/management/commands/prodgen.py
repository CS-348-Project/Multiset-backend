from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from glob import glob
import json
from os import makedirs
import re

from multiset.db_utils import execute_query
from multiset.seeding.query import get_seeding_query


class Command(BaseCommand):
    SAMPLE_TEST_PATH = "tests/suites/sample"
    PROD_TEST_PATH = "tests/suites/prod"

    help = "Runs all the tests in the tests directory and finds their expected output"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--noprint",
            action="store_true",
            help="Whether the result is printed",
        )

    def handle(self, *args, **kwargs):
        """
        Runs all the tests in the tests directory and finds their expected output

        The expected output should be between the lines "begin expected" and "end expected"
        in the SQL file. If it's not found, the test is marked as an error.

        Check `tests/sample_suite/test.sql` for an example of the expected output format

        TO RUN: `docker-compose run --rm web python manage.py querytest` (printing to files) or
        `docker-compose run --rm web python manage.py querytest --noprint` (no printing to files)

        """

        noprint = kwargs.get("noprint", False)

        passes = 0
        fails = []
        errors = []
        no_expected_output = 0

        # get the seeding query (ran before each test suite)
        seeding_query = get_seeding_query()

        # recursively get all the sql files in the tests directory
        files = glob(self.SAMPLE_TEST_PATH + "/**/*.sql", recursive=True)

        for file in files:
            print(f"Generating prod test for {file}")

            with open(file, encoding="utf8") as f:
                sql = f.read()

            splits = sql.split("\n")

            # get first split containing -- and prodorder

            pattern = r"\-\-\s*prodorder\s*(\S+)"
            prodorder = None

            for split in splits:
                match = re.search(pattern, split)

                if match:
                    prodorder = match.group(1)
                    break

            if prodorder is None:
                script = sql

            else:
                print("Ordering by", prodorder)

                semicolon_index = sql.find(";")

                # assume we have a semicolon
                script = sql[:semicolon_index]
                script += " ORDER BY " + prodorder
                script += " LIMIT 10;"

            # write it to a file
            output_path = self.PROD_TEST_PATH + file[len(self.SAMPLE_TEST_PATH) :]

            output_path = output_path.replace("\\", "/")

            makedirs(output_path[: output_path.rfind("/")], exist_ok=True)

            with open(output_path, "w") as f:
                f.write(script)
