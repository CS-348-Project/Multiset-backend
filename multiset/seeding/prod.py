from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from os import listdir
from os.path import join
import random
import pandas as pd
import math
import numpy as np

from optimization.services import calculate
from multiset.db_utils import execute_query
from multiset.seeding.template import *


class ProductionSeeder:
    CSV_PATH = join("multiset", "seeding", "prodcsv", "data.csv")

    MIN_GROUP_SIZE = 3
    MAX_GROUP_SIZE = 10

    UNIFORM_SPLIT_PROB = 0.7
    MEMBER_INCLUDE_PROB = 0.8

    SETTLEMENT_PROBABILITY = 0.5
    FULL_SETTLEMENT_PROBABILITY = 0.5
    MAX_SETTLEMENTS = 3

    CATEGORIES = [
        "Food",
        "Entertainment",
        "Rent",
        "Utilities",
        "Clothing",
        "Transportation",
        "Other",
    ]

    SEED = 123456

    def __init__(self):
        self.templates = multiset_templates()
        self.columns = {}
        self.rows = None

        # dicts to speed up lookups
        self.name_user_id = {}
        self.user_id_groups = {}
        self.group_id_users = {}
        self.purchase_id_splits = {}

        # ensure results are always the same
        random.seed(self.SEED)

    # Since the input data is huge, we won't seed things all at once
    def seed(self):
        # Read the data
        print("Reading data...")

        data = pd.read_csv(self.CSV_PATH)

        self.rows = data.values.tolist()

        for col in data.columns:
            self.columns[col] = len(self.columns)

        print("Processing users...")
        self._get_users()
        print(f"Seeding {len(self.templates['multiset_user'].rows)} users...")

        # with connection.cursor() as cursor:
        #     cursor.execute(str(self.templates["multiset_user"]))

        print("Processing groups and members...")
        self._get_groups()

        print(f"Seeding {len(self.templates['multiset_group'].rows)} groups...")

        # with connection.cursor() as cursor:
        #     cursor.execute(str(self.templates["multiset_group"]))
        #     print("Seeding members...")
        #     cursor.execute(str(self.templates["member"]))

        print("Processing purchases and splits...")

        self._get_purchases()

        print(f"Seeding {len(self.templates['purchase'].rows)} purchases...")

        # with connection.cursor() as cursor:
        #     cursor.execute(str(self.templates["purchase"]))
        #     print("Seeding splits...")
        #     cursor.execute(str(self.templates["purchase_splits"]))

        print(f"Calculating balances...")
        debt_dict = self._get_debts()

        print(f"Processing debts and settlements...")
        self._get_settlements(debt_dict)

        with connection.cursor() as cursor:
            print(f"Seeding {len(self.templates['cumulative_debts'].rows)} debts...")
            cursor.execute(str(self.templates["cumulative_debts"]))
            print(
                f"Seeding {len(self.templates['settlement_history'].rows)} settlements..."
            )
            cursor.execute(str(self.templates["settlement_history"]))

    def _get_users(self):
        users = self.templates["multiset_user"]

        names = []
        count = 0

        for row in self.rows:
            customer_name = row[self.columns["Customer_Name"]]
            # this has to be a string so we can hash it
            names.append(" ".join(self._get_first_last(customer_name)))

            name_split = customer_name.split(" ")

            # remove titles
            if name_split[0].endswith(".") or name_split[0] == "Miss":
                names.append(f"{name_split[1]} {name_split[2]}")
            else:
                names.append(f"{name_split[0]} {name_split[1]}")

            count += 1

        # get unique names
        names = list(set(names))
        user_id = 1

        for name in names:
            users.add_row(
                user_id,
                f"google{user_id}",
                f"{name.replace(' ', '').lower()}@gmail.com",
                name.split(" ")[0],
                name.split(" ")[1],
            )

            self.name_user_id[name] = user_id

            user_id += 1

    def _get_groups(self):
        # we ensure each user is in at least one group
        # each user can be in multiple groups
        user_count = len(self.templates["multiset_user"].rows)
        allotted_users = 0

        groups = self.templates["multiset_group"]
        members = self.templates["member"]
        group_id = 1

        while allotted_users < user_count:
            # this logic makes sure the last group isn't too small
            if user_count - allotted_users < 2 * self.MIN_GROUP_SIZE:
                group_size = user_count - allotted_users
            else:
                group_size = random.randint(self.MIN_GROUP_SIZE, self.MAX_GROUP_SIZE)

                while user_count - allotted_users - group_size < self.MIN_GROUP_SIZE:
                    group_size -= 1

            groups.add_row(group_id, f"Group {group_id}", random.choice([True, False]))

            self.group_id_users[group_id] = []

            for i in range(group_size):
                user_id = allotted_users + i + 1
                self.user_id_groups[user_id] = [group_id]
                self.group_id_users[group_id].append(user_id)

                members.add_row(user_id, group_id)

            group_id += 1

            allotted_users += group_size

        # also add some random groups
        new_groups = int(len(groups.rows) * 0.20)

        for i in range(new_groups):
            groups.add_row(group_id, f"Group {group_id}", random.choice([True, False]))

            member_ids = random.sample(
                range(1, user_count + 1),
                random.randint(self.MIN_GROUP_SIZE, self.MAX_GROUP_SIZE),
            )

            self.group_id_users[group_id] = []

            for member_id in member_ids:
                self.user_id_groups[member_id].append(group_id)
                self.group_id_users[group_id].append(member_id)
                members.add_row(member_id, group_id)

            group_id += 1

    def _get_purchases(self):
        # each row in the original csv corresponds to a purchase
        purchases = self.templates["purchase"]
        purchase_splits = self.templates["purchase_splits"]

        purchase_id = 1

        for row in self.rows:
            amount = row[self.columns["Total_Cost"]] * 100  # convert to cents
            purchaser_first, purchaser_last = self._get_first_last(
                row[self.columns["Customer_Name"]]
            )
            # get the purchaser id
            purchaser_id = self.name_user_id[f"{purchaser_first} {purchaser_last}"]

            # get all the groups the purchaser is in
            purchaser_groups = self.user_id_groups[purchaser_id]

            group_id = random.choice(purchaser_groups)
            category = random.choice(self.CATEGORIES)

            purchases.add_row(
                purchase_id,
                category,
                f"Purchase {purchase_id}",
                amount,
                purchaser_id,
                group_id,
            )

            # now, get the splits
            group_members = self.group_id_users[group_id]

            split_evenly = random.random() < self.UNIFORM_SPLIT_PROB
            remaining = amount

            self.purchase_id_splits[purchase_id] = []

            for i in range(len(group_members) - 1):
                if split_evenly:
                    split_amount = int(amount / len(group_members))
                else:
                    # using Gaussian makes splits more likely to be even-ish
                    mean = amount / len(group_members)
                    if mean > 1:
                        stdev = math.log(mean)
                    else:
                        stdev = mean

                    split_amount = int(random.gauss(mean, stdev))

                    if split_amount < 0:
                        split_amount = 0

                    if split_amount > remaining:
                        split_amount = remaining

                purchase_splits.add_row(
                    purchase_id,
                    group_members[i],
                    group_id,
                    split_amount,
                )

                self.purchase_id_splits[purchase_id].append(
                    {"user_id": group_members[i], "amount": split_amount}
                )

                remaining -= split_amount

            # no matter what, the last person gets the remainder
            # this is necessary even with even splits because of rounding
            purchase_splits.add_row(
                purchase_id,
                group_members[-1],
                group_id,
                remaining,
            )

            self.purchase_id_splits[purchase_id].append(
                {"user_id": group_members[-1], "amount": remaining}
            )

            purchase_id += 1

    def _get_debts(self):
        # we need to calculate the debts between users in a group
        # keys are tuples of (purchaser_id, borrower_id)
        debt_dict = {}

        for purchase in self.templates["purchase"].dict_rows:
            purchaser_id = purchase["purchaser_user_id"]

            for split in self.purchase_id_splits[purchase["id"]]:
                borrower_id = split["user_id"]
                amount = split["amount"]

                key = (purchaser_id, borrower_id, purchase["purchaser_group_id"])
                current_debt = debt_dict.get(key, 0)

                debt_dict[key] = current_debt + amount

        print("Calculating debts...")

        # we make a new dict to store the debts that have been cancelled out
        # we can't use the other bc we'd have to delete keys as we go which is illegal
        processed_debt_dict = {}

        # now, for every debt, see if the reverse debt exists
        for key in debt_dict:
            amount = debt_dict[key]
            reverse_pair = (key[1], key[0], key[2])
            reverse_amount = debt_dict.get((reverse_pair), None)

            if reverse_amount is not None:
                # if the reverse debt exists, we can cancel them out
                if amount > reverse_amount:
                    processed_debt_dict[key] = amount - reverse_amount

                elif amount < reverse_amount:
                    processed_debt_dict[reverse_pair] = reverse_amount - amount

        return processed_debt_dict

    def _get_settlements(self, debts: dict):
        settlements = self.templates["settlement_history"]
        cumulative_debts = self.templates["cumulative_debts"]
        settlement_id = 1

        for key in debts:
            pairwise_count = 0

            while (
                random.random() < self.SETTLEMENT_PROBABILITY
                and pairwise_count < self.MAX_SETTLEMENTS
                and debts[key] > 0
            ):
                if random.random() < self.FULL_SETTLEMENT_PROBABILITY:
                    amount = debts[key]

                else:
                    amount = random.randint(
                        0, int(debts[key])
                    )  # cast to int in case we have a float

                purchaser_id, borrower_id, group_id = key

                settlements.add_row(
                    settlement_id,
                    borrower_id,
                    group_id,
                    purchaser_id,
                    group_id,
                    amount,
                )

                debts[key] -= amount

                settlement_id += 1
                pairwise_count += 1

        for key in debts:
            if debts[key] > 0:
                purchaser_id, borrower_id, group_id = key

                cumulative_debts.add_row(
                    debts[key],
                    purchaser_id,
                    group_id,
                    borrower_id,
                    group_id,
                )

    @staticmethod
    def _get_first_last(name):
        name_split = name.split(" ")

        if name_split[0].endswith(".") or name_split[0] == "Miss":
            return name_split[1], name_split[2]

        return name_split[0], name_split[1]