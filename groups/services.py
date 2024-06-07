from multiset.db_utils import execute_query
from pathlib import Path
from typing import List

from .models import Group, GroupSkeleton

def create_group(group: GroupSkeleton, user_ids: List[int]):
    # user_ids_clause = ",".join([f"{user_id}" for user_id in user_ids])

    created_group = execute_query(
        Path("groups/sql/create_group.sql"),
        {"name": group.name, "optimize_payments": group.optimize_payments, "user_ids": user_ids},
    )
    # print("created_group", created_group, group.name, group.optimize_payments, user_ids)
    return {"status": "success"}

def get_group(group_id=None, member_id=None):
    rows = []
    if group_id:
      rows = execute_query(
          Path("groups/sql/get_groups_by_group_id.sql"),
          {"group_id": group_id},
          fetchall=True,
      )
    elif member_id:
      rows = execute_query(
          Path("groups/sql/get_groups_by_member_id.sql"),
          {"member_id": member_id},
          fetchall=True,
      )
    else:
        rows = execute_query(Path("groups/sql/get_groups.sql"), fetchall=True)
    return rows

def update_group(group: Group):
    updated_group = execute_query(
        Path("groups/sql/update_group.sql"),
        {"id": group.id, "name": group.name, "optimize_payments": group.optimize_payments},
    )
    return updated_group

def delete_group(group_id: int):
    deleted_group = execute_query(Path("groups/sql/delete_group.sql"), {"group_id": group_id})
    return deleted_group