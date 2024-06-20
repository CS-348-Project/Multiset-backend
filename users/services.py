from multiset.db_utils import execute_query
from pathlib import Path
from typing import List

from .models import User

def get_user(email = None, user_id = None):
    rows = []
    if email:
        rows = execute_query(
            Path("users/sql/get_users_by_email.sql"),
            {"email": email},
            fetchall=True,
        )
    elif user_id:
        rows = execute_query(
            Path("users/sql/get_users_by_user_id.sql"),
            {"user_id": user_id},
            fetchall=True,
        )
    else:
        rows = execute_query(Path("users/sql/get_users.sql"), fetchall=True)
    return rows
