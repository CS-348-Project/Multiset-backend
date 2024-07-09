from pathlib import Path
from member_activity_logs.models import MemberActivityLog
from multiset.db_utils import execute_query


def get_member_activity_logs_by_group_id(group_id: int) -> MemberActivityLog:
    logs = execute_query(
        Path("member_activity_logs/sql/get_member_activity_logs_by_group_id.sql"),
        {"group_id": group_id},
        fetchall=True)
    return logs