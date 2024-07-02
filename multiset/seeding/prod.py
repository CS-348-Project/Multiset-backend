from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from os import listdir
from os.path import join
from random import randint, choice, uniform
import pandas as pd
import numpy as np

from multiset.db_utils import execute_query
from multiset.seeding.template import *


class ProductionSeeder:
    CSV_PATH = join("multiset", "seeding", "prodcsv", "data.csv")

    def __init__(self):
        self.templates = multiset_templates()
        self.columns = {}
        self.rows = None

    # Since the input data is huge, we won't seed things all at once
    def seed(self):
        # Read the data
        print("Reading data...")

        data = pd.read_csv(self.CSV_PATH)

        # First we seed users
        # make up emails + google ids

        self.rows = data.values.tolist()

        for col in data.columns:
            self.columns[col] = len(self.columns)

        print("Processing users...")

        self._get_users()

        print(f"Seeding {len(self.templates['multiset_user'].rows)} users...")

        with connection.cursor() as cursor:
            cursor.execute(str(self.templates["multiset_user"]))

    def _get_users(self):
        users = self.templates["multiset_user"]

        names = []

        count = 0

        for row in self.rows:
            customer_name = row[self.columns["Customer_Name"]]
            name_split = customer_name.split(" ")

            # remove titles
            if name_split[0].endswith("."):
                name_split = name_split[1:]

            first_name = name_split[0]
            last_name = name_split[1]

            count += 1

            # needs to be string so we can hash it
            names.append(f"{first_name} {last_name}")

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
