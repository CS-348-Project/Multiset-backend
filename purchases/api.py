from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from purchases.models import Purchase
from purchases.services import new_purchase, split_purchase, valid_purchase

router = Router()


@router.get("/all-purchases")
def all_purchase_handler(request, group_id: int):
    """
    Returns all purchases from the database.
    Args:
        request: the HTTP request
    Returns:
        a JSON response with all purchases
    """
    purchases = execute_query(
        Path("purchases/sql/get_purchases_by_group_id.sql"),
        {"group_id": group_id},
        fetchall=True,
    )
    return JsonResponse(purchases, safe=False)


@router.get("/")
def get_purchase_handler(request, user_id: int, group_id: int = None):
    """
    Returns a purchases made by a user.
    Args:
        request: the HTTP request
        user_id: the ID of the user
        group_id: the ID of the group (optional)
    Returns:
        a JSON response with the purchase
    """
    if group_id:
        purchases = execute_query(
            Path("purchases/sql/get_purchases_by_user_id_and_group_id.sql"),
            {"user_id": user_id, "group_id": group_id},
            fetchall=True,
        )
    else:
        purchases = execute_query(
            Path("purchases/sql/get_purchases_by_user_id.sql"),
            {"user_id": user_id},
            fetchall=True,
        )
    return JsonResponse(purchases, safe=False)

@router.get("/recurring_purchases")
def get_recurring_purchase_handler(request, user_id: int):
    """
    Returns the recurring purchase items of a user.
    Args:
        user_id: the ID of the user
    Returns:
        a JSON response with recurring purchase item name
    """
    recurring_purchases = execute_query(
            Path("purchases/sql/get_recurring_purchases.sql"),
            {"user_id": user_id},
            fetchall=True,
        )
    return JsonResponse(recurring_purchases, safe=False)

@router.post("/new-purchase")
def create_new_purchase(request, purchase: Purchase):
    """
    Creates a new purchase and its splits in the database.
    Args:
        purchase: the purchase object to be created and a list of purchase splits
    Returns:
        a JSON response with the status of the operation
    """
    user_id = request.auth
    purchase.purchaser = user_id
    if not valid_purchase(purchase):
        return JsonResponse({"status": "error", "message": "Purchase is not valid"}, status=400)
    created_purchase = new_purchase(purchase)
    new_purchase_id = created_purchase["id"]
    split_purchase(purchase, new_purchase_id)

    return JsonResponse({}, status=204)


@router.get("/purchase_splits/{purchase_id}")
def get_purchase_splits_by_id(request, purchase_id: int):
    """
    Returns a purchase by its ID.
    Args:
        request: the HTTP request
        purchase_id: the ID of the purchase
    Returns:
        a JSON response with the purchase
    """
    purchase = execute_query(
        Path("purchases/sql/get_purchase_splits_by_purchase_id.sql"),
        {"purchase_id": purchase_id},
        fetchall=True,
    )
    return JsonResponse(purchase, safe=False)


@router.get("/purchase_details/{purchase_id}")
def get_purchase_by_id(request, purchase_id: int):
    """
    Returns a purchase by its ID.
    Args:
        request: the HTTP request
        purchase_id: the ID of the purchase
    Returns:
        a JSON response with the purchase
    """
    purchase = execute_query(
        Path("purchases/sql/get_purchase_by_id.sql"),
        {"purchase_id": purchase_id},
        fetchone=True,
    )
    return JsonResponse(purchase, safe=False)
