from multiset.db_utils import execute_query
from pathlib import Path


def get_purchase_category_count(group_id: int):
    rows = execute_query(
        Path("analytics/sql/get_purchase_category_count.sql"),
        {"group_id": group_id},
        fetchall=True,
    )
    return rows
