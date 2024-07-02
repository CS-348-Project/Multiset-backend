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
        def _get_value_string(value):
            if type(value) == str:
                return f"'{value}'"
            elif type(value) == bool:
                return str(value).upper()
            elif value == None:
                return "NULL"
            else:
                return str(value)

        sql = f"DELETE FROM {self.table};\n"
        sql += f"INSERT INTO {self.table} ({', '.join(self.columns)}) VALUES\n"

        sql += "".join(
            [
                f"({', '.join([_get_value_string(value) for value in row])}),\n"
                for row in self.rows
            ]
        )

        sql = sql[:-2] + ";\n"

        # if we have an id column, we need to reset the serial so new rows start from the correct id
        if "id" in self.columns:
            sql += f"SELECT setval('{self.table}_id_seq', (SELECT MAX(id) FROM {self.table}));\n"

        return sql


def multiset_templates():
    # this is a function so each invocation returns new template objects
    return {
        "multiset_user": SeedingTemplate(
            "multiset_user", ("id", "google_id", "email", "first_name", "last_name")
        ),
        "multiset_group": SeedingTemplate(
            "multiset_group", ("id", "name", "optimize_payments")
        ),
        "member": SeedingTemplate("member", ("user_id", "group_id")),
        "purchase": SeedingTemplate(
            "purchase",
            (
                "id",
                "category",
                "name",
                "total_cost",
                "purchaser_user_id",
                "purchaser_group_id",
            ),
        ),
        "purchase_splits": SeedingTemplate(
            "purchase_splits",
            ("purchase_id", "borrower_user_id", "borrower_group_id", "amount"),
        ),
        "cumulative_debts": SeedingTemplate(
            "cumulative_debts",
            (
                "amount",
                "collector_user_id",
                "collector_group_id",
                "borrower_user_id",
                "borrower_group_id",
            ),
        ),
        "settlement_history": SeedingTemplate(
            "settlement_history",
            (
                "id",
                "sender_user_id",
                "sender_group_id",
                "receiver_user_id",
                "receiver_group_id",
                "amount",
            ),
        ),
        "grocery_list": SeedingTemplate("grocery_list", ("id", "group_id", "name")),
        "grocery_list_item": SeedingTemplate(
            "grocery_list_item",
            (
                "id",
                "grocery_list_id",
                "requester_user_id",
                "requester_group_id",
                "completed",
                "notes",
                "quantity",
                "item_name",
            ),
        ),
    }
