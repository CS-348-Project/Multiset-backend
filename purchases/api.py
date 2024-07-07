from groups.services import verify_user_in_group
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
    try: 
        verify_user_in_group(request.auth, group_id)
        purchases = execute_query(
            Path("purchases/sql/get_purchases_by_group_id.sql"),
            {"group_id": group_id},
            fetchall=True,
        )
        return JsonResponse(purchases, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching purchases"}, status=500)


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
    try:
        if group_id:
            verify_user_in_group(request.auth, group_id)
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
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching purchases"}, status=500)


@router.post("/new-purchase")
def create_new_purchase(request, purchase: Purchase):
    """
    Creates a new purchase and its splits in the database.
    Args:
        purchase: the purchase object to be created and a list of purchase splits
    Returns:
        a JSON response with the status of the operation
    """
    try:
        user_id = request.auth
        verify_user_in_group(user_id, purchase.group_id)
        purchase.purchaser = user_id
        if not valid_purchase(purchase):
            return JsonResponse({"status": "error", "message": "Purchase is not valid"}, status=400)
        created_purchase = new_purchase(purchase)
        new_purchase_id = created_purchase["id"]
        split_purchase(purchase, new_purchase_id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in creating purchase"}, status=500)