from ninja import Schema
from typing import List, Optional


class PurchaseSplit(Schema):
    amount: int
    borrower: int


class Purchase(Schema):
    name: str
    category: str
    group_id: int
    total_cost: int
    purchaser: Optional[int] = None
    purchase_splits: List[PurchaseSplit]
