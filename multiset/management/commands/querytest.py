from django.core.management.base import BaseCommand, CommandParser
from glob import glob
import json
from os import makedirs

from multiset.db_utils import execute_query

import sys


class Command(BaseCommand):
    TEST_PATH = "tests/suites/"
    OUTPUT_PATH = "tests/outputs/"

    help = "Runs all the tests in the tests directory and finds their expected output"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--print",
            action="store_true",
            help="Whether the result is printed",
        )

    def handle(self, *args, **kwargs):
        """
        Runs all the tests in the tests directory and finds their expected output

        The expected output should be between the lines "begin expected" and "end expected"
        in the SQL file. If it's not found, the test is marked as an error.

        Check `tests/sample_suite/test.sql` for an example of the expected output format

        TO RUN: `docker-compose run web python manage.py querytest` (no printing to files) or
        `docker-compose run web python manage.py querytest --print` (with printing to files)

        """

        print_to_file = kwargs.get("print", False)

        passes = 0
        fails = []
        errors = []

        # recursively get all the sql files in the tests directory
        files = glob(self.TEST_PATH + "/**/*.sql", recursive=True)

        print(f"Running {len(files)} test(s)...")

        for file in files:
            # TODO error handling and reporting

            # now, we get the result of the query
            raw_result = execute_query(file, fetchall=True)

            # let's get the expected output
            with open(file, "r") as f:
                contents = f.read()

            content_lines = contents.split("\n")

            # get the expected output or return an error if it doesn't exist
            # side note, the ./E/F printing is how regular Django tests work and I'm stealing it
            try:
                start = content_lines.index("begin expected") + 1
                end = content_lines.index("end expected") - 1

                if start > end:
                    raise ValueError("Invalid expected output range")

                expected_output_str = "\n".join(content_lines[start : end + 1])
                expected_output_obj = json.loads(expected_output_str)

                if expected_output_obj == raw_result:
                    print(".", end="")
                    passes += 1

                else:
                    print("F", end="")
                    fails.append(
                        {
                            "file": file,
                            "result": json.dumps(raw_result, indent=4, default=str),
                            "expected": expected_output_str,
                        }
                    )

                print()

            # no expected output found
            # for now we just skip the test but still print if appropriate
            except ValueError:
                pass

            # this just replaces self.TEST_PATH with self.OUTPUT_PATH and changes the extension
            output_path = f"{self.OUTPUT_PATH}{file[len(self.TEST_PATH):-4]}.out"

            # create the directory if it doesn't exist
            # we remove the file name from the path to get the directory
            makedirs(output_path[: output_path.rfind("/")], exist_ok=True)

            if print_to_file:
                with open(output_path, "w") as f:
                    json.dump(raw_result, f, indent=4, default=str)

        # print the detailed results
        print(f"Passes: {passes}, Fails: {len(fails)}, Errors: {len(errors)}")

        if len(fails) > 0:
            print("Fails:")
            for fail in fails:
                print(f"File: {fail['file']}")
                print("Expected:")
                print(fail["expected"])
                print("Result:")
                print(fail["result"])

        if len(errors) > 0:
            print("Errors:")
            for error in errors:
                print(f"{error} (no expected output found in SQL file)")

    def _to_csv(self, result: list) -> str:
        # convert the result to a csv string
        if len(result) == 0:
            return "[]"  # special case for empty result so it's more clear

        csv = ",".join(result[0].keys()) + "\n"
        for row in result:
            csv += ",".join(map(str, row.values())) + "\n"

        # remove the last newline
        return csv[:-1]
    