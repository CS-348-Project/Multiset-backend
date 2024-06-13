from django.core.management.base import BaseCommand
from multiset.db_utils import execute_query
from glob import glob


class Command(BaseCommand):
    TEST_PATH = "tests/"

    def handle(self, *args, **kwargs):
        passes = 0
        fails = []
        errors = []

        # get all the sql files in the tests directory
        files = glob(self.TEST_PATH + "/**/*.sql", recursive=True)

        print(f"Running {len(files)} tests...")

        for file in files:
            # let's get the expected output
            with open(file, "r") as f:
                contents = f.read()

            content_lines = contents.split("\n")

            # get the expected output or return an error if it doesn't exist
            try:
                start = content_lines.index("begin expected") + 1
                end = content_lines.index("end expected") - 1

                if start >= end:
                    raise ValueError("Invalid expected output range")
            except ValueError:
                print("E", end="")
                errors.append(file)
                continue

            expected_output = "\n".join(content_lines[start : end + 1])

            # now, we get the result of the query
            raw_result = execute_query(file, fetchall=True)
            string_result = self._to_csv(raw_result)

            if string_result == expected_output:
                print(".", end="")
                passes += 1

            else:
                print("F", end="")
                fails.append(
                    {"file": file, "result": string_result, "expected": expected_output}
                )

        print()
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
            return "[]"  # special case for empty result

        csv = ",".join(result[0].keys()) + "\n"
        for row in result:
            csv += ",".join(map(str, row.values())) + "\n"

        # remove the last newline
        return csv[:-1]
