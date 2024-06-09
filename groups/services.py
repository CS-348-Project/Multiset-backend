from multiset.db_utils import execute_query
from pathlib import Path
from typing import List

from .models import Group, GroupSkeleton

def create_group(group: GroupSkeleton, user_ids: List[int]):
    created_group = execute_query(
        Path("groups/sql/create_group.sql"),
        {"name": group.name, "optimize_payments": group.optimize_payments, "budget": group.budget, "user_ids": user_ids},
    )
    return {"status": "success"}

def get_group(group_id=None, user_id=None):
    rows = []
    if group_id:
      rows = execute_query(
          Path("groups/sql/get_groups_by_group_id.sql"),
          {"group_id": group_id},
          fetchall=True,
      )
    elif user_id:
      rows = execute_query(
          Path("groups/sql/get_groups_by_user_id.sql"),
          {"user_id": user_id},
          fetchall=True,
      )
    else:
        rows = execute_query(Path("groups/sql/get_groups.sql"), fetchall=True)
    return rows

def update_group(group: Group):
    updated_group = execute_query(
        Path("groups/sql/update_group.sql"),
        {"group_id": group.id, "name": group.name, "optimize_payments": group.optimize_payments, "budget": group.budget},
    )
    return updated_group

def delete_group(group_id: int):
    deleted_group = execute_query(Path("groups/sql/delete_group.sql"), {"group_id": group_id})
    return deleted_group