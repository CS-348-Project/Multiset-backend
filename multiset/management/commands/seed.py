from django.core.management.base import BaseCommand
from django.db import connection
from os import listdir
from os.path import join
from random import randint, choice, uniform
import pandas as pd

from multiset.seeding import *


class Command(BaseCommand):
    """
    Making this a command allows us to run it in the same way we
    run other scripts (i.e. python manage.py seed)
    """

    CSV_PATH = join("multiset", "management", "commands", "csv")

    help = "Seeds the database with randomized dummy data."

    def handle(self, *args, **kwargs):
        print("Deleting existing data...")
        files = listdir(self.CSV_PATH)

        with connection.cursor() as cursor:
            for file in files:
                cursor.execute(f"DELETE FROM {file[:-4]};")

        print("Seeding the database...")
        tables: dict[str, SeedingTemplate] = {}

        for file in files:
            path = join(self.CSV_PATH, file)
            table_raw = pd.read_csv(path)

            table = SeedingTemplate(file[:-4], tuple(table_raw.columns.to_list()))

            if file == "purchase_splits.csv":
                # i tried to do this with pandas but it wasnt working and im annoyed
                # this is just to correct the types of the values
                processed_values = table_raw.values.tolist()

                for row in processed_values:
                    table.add_row(
                        int(row[0]), int(row[1]), round(row[2], 2), int(row[3])
                    )
            else:
                table.rows = table_raw.values.tolist()

            tables[file[:-4]] = table

        debts = []

        # now, let's get our collective debt data
        # this is lowkey inefficient but it's fine
        for row in tables["purchase_splits"].dict_rows:
            # get the purchaser from the associated purchase
            # next returns the first element that matches the criteria

            purchaser = next(
                purchase
                for purchase in tables["purchase"].dict_rows
                if purchase["id"] == row["purchase_id"]
            )["purchaser"]

            try:
                # if the debt already exists, add to it
                debt = next(
                    debt
                    for debt in debts
                    if debt["borrower_id"] == row["borrower"]
                    and debt["purchaser_id"] == purchaser
                )
                debt["amount"] += row["amount"]

            except StopIteration:
                # if the debt doesn't exist, create it and append to our list
                debt = {
                    "borrower_id": row["borrower"],
                    "purchaser_id": purchaser,
                    "amount": row["amount"],
                }
                debts.append(debt)

        debt_rows = [
            (i, round(debt["amount"], 2), debt["borrower_id"], debt["purchaser_id"])
            for i, debt in enumerate(debts)
        ]

        tables["cumulative_debts"].rows = debt_rows

        # finally, we are done!
        print("Done loading seeding data. Printing script...")

        # now we insert the data into the database
        # we have to do this in a specific order because of foreign key constraints
        script = f"""{str(tables['multiset_user'])}\n
                        {str(tables['multiset_group'])}\n
                        {str(tables['member'])}\n
                        {str(tables['purchase'])}\n
                        {str(tables['purchase_splits'])}\n
                        {str(tables['cumulative_debts'])}\n
                        {str(tables['settlement_history'])}"""

        print(script)

        # Please actually briefly look over the data to make sure nothing is wrong :,)
        print("Press enter to continue...")
        input()

        with connection.cursor() as cursor:
            cursor.execute(script)
            pass

        print("Done seeding the database.")


# Below is partially finished code for making randomized data in case we decide to use it later
# User, group, member, and purchase data is generated, but not the splits.

# USER_COUNT = 20
# GROUP_COUNT = 7
# PURCHASE_COUNT = 50

# permissible ranges for the cost of purchases in each category
# CATEGORY_RANGES = {
#     "Food": (5, 80),
#     "Rent": (100, 1000),
#     "Utilities": (10, 100),
#     "Entertainment": (5, 200),
#     "Other": (1, 100),
# }

# def handle(self, *args, **kwargs):
#     # TODO take input from user for number of rows?
#     print("Seeding the database...")
#     self._generate_users()
#     self._generate_groups()
#     self._generate_purchases()

# def _generate_users(self):
#     for i in range(self.USER_COUNT):
#         userScript.add_row(
#             i,  # id
#             f"user{i}+{self._random_alphanumeric(3)}",  # user_token (can be changed once we know how auth is happening)
#             self._random_email(),  # email
#             self._random_alphanumeric(10),  # password
#         )

# def _generate_groups(self):
#     for i in range(self.GROUP_COUNT):
#         groupScript.add_row(
#             i,  # id
#             f"group{i}",  # name
#             bool(randint(0, 1)),  # optimize_payments
#         )

#     # now we make members: we have 4 "main" groups that include everyone once, and 3 groups with a few random members
#     for i in range(self.USER_COUNT):
#         memberScript.add_row(i, i, i % 4)  # id, user_id, group_id

#     id = self.USER_COUNT

#     for i in range(4, self.GROUP_COUNT):
#         members = [randint(0, self.USER_COUNT - 1) for _ in range(randint(2, 4))]
#         members = set(members)  # no duplicates
#         for member in members:
#             memberScript.add_row(id, member, i)
#             id += 1

# def _generate_purchases(self):
#     for i in range(self.PURCHASE_COUNT):
#         category = choice(list(self.CATEGORY_RANGES.keys()))
#         cost = randint(*self.CATEGORY_RANGES[category])
#         cost += randint(0, 99) / 100  # add some cents

#         group_id = randint(0, self.GROUP_COUNT - 1)
#         group_members = [
#             member[1] for member in memberScript.rows if member[2] == group_id
#         ]

#         purchaser = choice(group_members)

#         purchaseScript.add_row(
#             i,  # id
#             f"purchase{i}",  # name
#             category,  # category
#             group_id,  # group_id
#             cost,  # total_cost
#             purchaser,  # purchaser
#         )

#         # now we have to add splits
#         remaining_cost = cost
#         for member in group_members:
#             if member == purchaser:
#                 continue

#             if uniform(0, 1) > 0.7:
#                 split = round(uniform(0, remaining_cost), 2)
#                 remaining_cost -= split

#             purchaseSplitsScript.add_row(
#                 i * self.PURCHASE_COUNT + member, i, split, member
#             )  # id, purchase_id, amount, borrower

#     print(purchaseScript)
#     print(purchaseSplitsScript)

# def _random_email(self):
#     # Let's at least try to make these human-readable
#     vowels = "aeiou"
#     consonants = "bcdfghjklmnpqrstvwxyz"

#     return f"{choice(consonants)}{choice(vowels)}{choice(consonants)}{randint(100, 999)}@gmail.com"

# def _random_alphanumeric(self, length: int):
#     chars = "abcdefghijklmnopqrstuvwxyz0123456789"
#     return "".join(choice(chars) for _ in range(length))
