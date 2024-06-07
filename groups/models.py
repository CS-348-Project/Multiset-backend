from ninja import Schema
from typing import List, Optional

class GroupSkeleton(Schema):
    name: str
    optimize_payments: bool
    budget: Optional[int]

class Group(Schema):
    id: int
    created_at: str
    name: str
    optimize_payments: bool
    budget: Optional[int]


    