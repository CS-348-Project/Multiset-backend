from multiset.db_utils import execute_query
from pathlib import Path


def find_settlements():
    rows = execute_query(Path("settlements/sql/get_settlements.sql"), fetchall=True)
    if rows:
        return rows
    return None


def save_settlement(purchaser_id, amount, borrower_id):
    execute_query(
        Path("settlements/sql/add_settlements.sql"), [purchaser_id, amount, borrower_id]
    )
    return True
