from multiset.db_utils import execute_query
from pathlib import Path
from typing import List

from .models import Group, GroupSkeleton

def create_group(group: GroupSkeleton, user_ids: List[int]):
    created_group = execute_query(
        Path("groups/sql/create_group/create_group.sql"),
        {"name": group.name, "optimize_payments": group.optimize_payments},
        fetchone=True,
    )
    execute_query(
        Path("groups/sql/create_group/add_users_to_group.sql"),
        {"group_id": created_group["id"], "user_ids": user_ids},
    )
    return created_group

def get_group(group_id=None, user_id=None, detailed=False):
    rows = []
    if group_id:
        if detailed:
            rows = execute_query(
                Path("groups/sql/get_groups_by_group_id_detailed.sql"),
                {"group_id": group_id},
                fetchone=True,
            )
        else:
            rows = execute_query(
                Path("groups/sql/get_groups_by_group_id.sql"),
                {"group_id": group_id, "detailed": detailed},
                fetchone=True,
            )
    elif user_id:
        if detailed:
            rows = execute_query(
                Path("groups/sql/get_groups_by_user_id_detailed.sql"),
                {"user_id": user_id},
                fetchall=True,
            )
        else:
            rows = execute_query(
                Path("groups/sql/get_groups_by_user_id.sql"),
                {"user_id": user_id, "detailed": detailed},
                fetchall=True,
            )
    return rows

def update_group(group: Group):
    updated_group = execute_query(
        Path("groups/sql/update_group.sql"),
        {"group_id": group.id, "name": group.name, "optimize_payments": group.optimize_payments},
    )
    return updated_group

def delete_group(group_id: int):
    deleted_group = execute_query(Path("groups/sql/delete_group.sql"), {"group_id": group_id})
    return deleted_group

def verify_user_in_group(user_id: int, group_id: int):
    res = execute_query(
        Path("groups/sql/verify_user_in_group.sql"),
        {"user_id": user_id, "group_id": group_id},
        fetchone=True,
    )
    return res.get("count") > 0