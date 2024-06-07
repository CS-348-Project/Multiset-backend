from ninja import Schema
from typing import List

class GroupSkeleton(Schema):
    name: str
    optimize_payments: bool
    # budget: int

class Group(Schema):
    id: int
    name: str
    optimize_payments: bool
    # budget: int


    