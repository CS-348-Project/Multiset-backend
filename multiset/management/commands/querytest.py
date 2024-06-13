from django.core.management.base import BaseCommand
from multiset.db_utils import execute_query
from glob import glob


class Command(BaseCommand):
    TEST_PATH = "tests/"

    def handle(self, *args, **kwargs):
        passes = 0
        fails = 0
        errors = 0

        # get all the sql files in the tests directory
        files = glob(self.TEST_PATH + "/**/*.sql", recursive=True)

        for file in files:
            raw_result = execute_query(file, fetchall=True)
            string_result = self._to_csv(raw_result)

            # now, let's compare with the expected output
            with open(file, "r") as f:
                contents = f.read()

            content_lines = contents.split("\n")

            # get the expected output
            try:
                start = content_lines.index("begin expected") + 1
                end = content_lines.index("end expected") - 1
            except ValueError:
                print("E", end="")
                errors += 1
                continue

            expected_output = "\n".join(content_lines[start : end + 1])

            if string_result == expected_output:
                print(".", end="")
                passes += 1

            else:
                print("F", end="")
                fails += 1

        print()
        print(f"Passes: {passes}, Fails: {fails}, Errors: {errors}")

    def _to_csv(self, result: list) -> str:
        # convert the result to a csv string
        if len(result) == 0:
            return "[]"  # special case for empty result

        csv = ",".join(result[0].keys()) + "\n"
        for row in result:
            csv += ",".join(map(str, row.values())) + "\n"

        # remove the last newline
        return csv[:-1]
