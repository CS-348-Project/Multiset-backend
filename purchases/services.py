from multiset.db_utils import execute_query
from purchases.models import Purchase
from django.http import JsonResponse
from pathlib import Path


def valid_purchase(purchase: Purchase):
    """
    Args:
        The new purchase object
    Returns:
        True if the purchase is valid otherwise False
    """
    sum = 0
    for purchase_split in purchase.purchase_splits:
        sum += purchase_split.amount
    if sum != purchase.total_cost:
        return False
    return True


def new_purchase(purchase: Purchase):
    """
    Inserts the purchase into the relation and checks that it was properly inserted
    Args:
        The new purchase object
    Returns:
        Dictionary with {id}
    """
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
    """
    Iterates through the people that split the purchase and populates the purchase_splits table

    Args:
        purchase: the new purchase object
        new_purchase_id: the id of the purchase that the splits are associated with
    Returns:
        None
    """
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
