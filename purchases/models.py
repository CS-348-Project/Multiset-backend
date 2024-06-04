from ninja import Schema
from typing import List


class PurchaseSplit(Schema):
    amount: int
    borrower: int


class Purchase(Schema):
    name: str
    category: str
    group_id: int
    total_cost: int
    purchaser: int
    purchase_splits: List[PurchaseSplit]
