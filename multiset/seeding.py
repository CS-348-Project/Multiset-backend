class SeedingTemplate:
    """
    Utility class to create seeding scripts for the database.
    Does not do any validation on the input data (but does insert different types properly).
    """

    def __init__(self, table: str, columns: tuple[str]):
        self.table = table
        self.columns = columns
        self.rows = []

    def add_row(self, *row):
        assert len(row) == len(self.columns)
        self.rows.append(row)

        # allow chaining
        return self

    @property
    def dict_rows(self):
        return [dict(zip(self.columns, row)) for row in self.rows]

    def __str__(self):
        sql = f"DELETE FROM {self.table};\n"
        sql += f"INSERT INTO {self.table} ({', '.join(self.columns)}) VALUES\n"

        for row in self.rows:
            row_str = "("

            for value in row:
                # we have to handle each value individually because they can be all different types

                if type(value) == str:
                    row_str += f"'{value}', "

                elif type(value) == bool:
                    row_str += f"{str(value).upper()}, "

                elif value == None:
                    row_str += "NULL, "

                else:
                    row_str += f"{value}, "

            row_str = row_str[:-2] + "),\n"

            sql += row_str

        sql = sql[:-2] + ";\n"

        # if we have an id column, we need to reset the serial so new rows start from the correct id
        if "id" in self.columns:
            sql += f"SELECT setval('{self.table}_id_seq', (SELECT MAX(id) FROM {self.table}));\n"

        return sql
