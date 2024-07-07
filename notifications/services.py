from pathlib import Path

from multiset.db_utils import execute_query


def get_notifications(user_id: int):
    return execute_query(
        Path("notifications/sql/get.sql"),
        {"user_id": user_id},
        fetchall=True,
    )


def read_notifications(user_id: int):
    return execute_query(
        Path("notifications/sql/read.sql"),
        {"user_id": user_id},
    )


def delete_notifications(user_id: int):
    return execute_query(
        Path("notifications/sql/clear.sql"),
        {"user_id": user_id},
    )
