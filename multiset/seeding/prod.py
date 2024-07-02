from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from os import listdir
from os.path import join
import random
import pandas as pd
import numpy as np

from multiset.db_utils import execute_query
from multiset.seeding.template import *


class ProductionSeeder:
    CSV_PATH = join("multiset", "seeding", "prodcsv", "data.csv")

    MIN_GROUP_SIZE = 3
    MAX_GROUP_SIZE = 10
    SEED = 123456

    def __init__(self):
        self.templates = multiset_templates()
        self.columns = {}
        self.rows = None

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

        with connection.cursor() as cursor:
            cursor.execute(str(self.templates["multiset_user"]))

        print("Processing groups and members...")
        self._get_groups()

        print(f"Seeding {len(self.templates['multiset_group'].rows)} groups...")

        with connection.cursor() as cursor:
            cursor.execute(str(self.templates["multiset_group"]))

        print(f"Seeding {len(self.templates['member'].rows)} members...")

        with connection.cursor() as cursor:
            cursor.execute(str(self.templates["member"]))

    def _get_users(self):
        users = self.templates["multiset_user"]
        # holds strings so we can hash them

        names = []
        count = 0

        for row in self.rows:
            customer_name = row[self.columns["Customer_Name"]]
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

            for i in range(group_size):
                members.add_row(allotted_users + i + 1, group_id)

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

            for member_id in member_ids:
                members.add_row(member_id, group_id)

            group_id += 1
