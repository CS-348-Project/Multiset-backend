from django.core.management.base import BaseCommand, CommandParser
from django.db import connection
from os import listdir
from os.path import join
from random import randint, choice, uniform
import pandas as pd
import numpy as np

from multiset.seeding.template import *

CSV_PATH = join("multiset", "seeding", "csv")


def get_seeding_query():
    files = listdir(CSV_PATH)

    print("Getting seeding query...")
    tables: dict[str, SeedingTemplate] = {}

    for file in files:
        path = join(CSV_PATH, file)
        table_raw = pd.read_csv(path)

        table = SeedingTemplate(file[:-4], tuple(table_raw.columns.to_list()))

        if file == "purchase_splits.csv":
            # i tried to do this with pandas but it wasnt working and im annoyed
            # this is just to correct the types of the values
            processed_values = table_raw.values.tolist()

            for row in processed_values:
                table.add_row(int(row[0]), int(row[1]), round(row[2], 2), int(row[3]))

        elif file == "grocery_list_item.csv":
            # we have to handle NaN values in the "notes" column
            # these occur when this column is empty in a given row
            processed_values = table_raw.values.tolist()

            for row in processed_values:
                try:
                    if np.isnan(row[5]):
                        row[5] = None
                except TypeError:  # happens when the value is a string, can ignore
                    pass

                table.add_row(*row)
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
        )

        try:
            # if the debt already exists, add to it
            debt = next(
                debt
                for debt in debts
                if debt["borrower_user_id"] == row["borrower_user_id"]
                and debt["borrower_group_id"] == row["borrower_group_id"]
                and debt["purchaser_user_id"] == purchaser["purchaser_user_id"]
                and debt["purchaser_group_id"] == purchaser["purchaser_group_id"]
            )
            debt["amount"] += row["amount"]

        except StopIteration:
            # if the debt doesn't exist, create it and append to our list
            debt = {
                "borrower_user_id": row["borrower_user_id"],
                "borrower_group_id": row["borrower_group_id"],
                "purchaser_user_id": purchaser["purchaser_user_id"],
                "purchaser_group_id": purchaser["purchaser_group_id"],
                "amount": row["amount"],
            }
            debts.append(debt)

    debt_rows = [
        (
            debt["amount"],
            debt["purchaser_user_id"],
            debt["purchaser_group_id"],
            debt["borrower_user_id"],
            debt["borrower_group_id"],
        )
        for debt in debts
    ]

    tables["cumulative_debts"].rows = debt_rows

    # finally, we are done!
    # now we insert the data into the database
    # we have to do this in a specific order because of foreign key constraints
    script = f"""
                    {str(tables['member_activity_logs'])}\n
                    {str(tables['notification'])}
                    {str(tables['multiset_user'])}\n
                    {str(tables['multiset_group'])}\n
                    {str(tables['member'])}\n
                    {str(tables['purchase'])}\n
                    {str(tables['purchase_splits'])}\n
                    {str(tables['cumulative_debts'])}\n
                    {str(tables['grocery_list'])}\n
                    {str(tables['grocery_list_item'])}\n
                    {str(tables['settlement_history'])}"""

    return script
