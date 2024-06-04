from multiset.db_utils import execute_query
from purchases.models import Purchase
from django.http import JsonResponse
from pathlib import Path


def new_purchase(purchase: Purchase):
    new_purchase = execute_query(
        Path("purchases/sql/new_purchase.sql"),
        {
            "name": purchase.name,
            "category": purchase.category,
            "group_id": purchase.group_id,
            "total_cost": purchase.total_cost,
            "purchaser": purchase.purchaser,
        },
        fetchone=True,
    )
    if not new_purchase:
        return JsonResponse({"status": "error, purchase_id not found"})
    return new_purchase


def split_purchase(purchase: Purchase, new_purchase_id):
    for purchase_split in purchase.purchase_splits:
        execute_query(
            Path("purchases/sql/split_purchase.sql"),
            {
                "purchase_id": new_purchase_id,
                "amount": purchase_split.amount,
                "borrower": purchase_split.borrower,
            },
            fetchone=True,
        )
