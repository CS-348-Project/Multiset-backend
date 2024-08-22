from datetime import datetime
from ninja import Schema
from typing import List, Optional


class GroupSkeleton(Schema):
    name: str
    optimize_payments: Optional[bool] = True


class CreateGroup(Schema):
    group_info: GroupSkeleton
    user_ids: List[int] = []


class Group(Schema):
    id: int
    created_at: datetime
    name: str
    optimize_payments: bool
    share_code: str


class GroupMembers(Schema):
    group_id: int
    user_ids: List[int]
