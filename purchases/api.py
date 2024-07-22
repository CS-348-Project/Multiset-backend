from groups.services import verify_user_in_group
from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from purchases.models import Purchase
from purchases.services import (
    new_purchase,
    split_purchase,
    valid_purchase,
    get_purchase_by_id,
    get_purchase_splits,
)

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
    if not verify_user_in_group(request.auth, group_id):
        return JsonResponse(
            {"status": "error", "message": "You are unauthorized to access this group"},
            status=403,
        )
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
        if not verify_user_in_group(request.auth, group_id):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "You are unauthorized to access this group",
                },
                status=403,
            )
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
        return JsonResponse(
            {"status": "error", "message": "Purchase splits do not sum up to total"},
            status=400,
        )
    created_purchase = new_purchase(purchase)
    new_purchase_id = created_purchase["id"]
    split_purchase(purchase, new_purchase_id)

    return JsonResponse({}, status=204)


@router.get("/purchase_splits")
def get_purchase_splits_by_id(request, purchase_id: int):
    """
    Returns a purchase by its ID.
    Args:
        request: the HTTP request
        purchase_id: the ID of the purchase
    Returns:
        a JSON response with the purchase
    """
    purchase = get_purchase_by_id(purchase_id)
    if purchase and not verify_user_in_group(
        request.auth, purchase.get("purchaser_group_id")
    ):
        return JsonResponse(
            {"status": "error", "message": "You are unauthorized to access this group"},
            status=403,
        )
    purchase_splits = get_purchase_splits(purchase_id)
    return JsonResponse(purchase_splits, safe=False)


@router.get("/purchase_details")
def get_purchase_details(request, purchase_id: int):
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
    if purchase and not verify_user_in_group(
        request.auth, purchase.get("purchaser_group_id")
    ):
        return JsonResponse(
            {"status": "error", "message": "You are unauthorized to access this group"},
            status=403,
        )
    return JsonResponse(purchase, safe=False)


@router.get("/purchase_form_details")
def get_all_purchase_details(request, purchase_id: int):
    """
    Returns a purchase and its splits by its ID.
    Args:
        request: the HTTP request
        purchase_id: the ID of the purchase
    Returns:
        a JSON response with the purchase and its splits
    """
    purchase = get_purchase_by_id(purchase_id)
    purchase_splits = get_purchase_splits(purchase_id)
    formatted_purchase_split = []
    for purchase_split in purchase_splits:
        formatted_purchase_split.append(
            {
                "borrower": purchase_split["id"],
                "amount": round(purchase_split["amount"] / 100, 2),
            }
        )
    res = {
        "name": purchase["name"],
        "category": purchase["category"],
        "total_cost": round(purchase["total_cost"] / 100, 2),
        "group_id": purchase["purchaser_group_id"],
        "purchase_splits": formatted_purchase_split,
    }
    return JsonResponse(res, safe=False)


@router.delete("/delete_purchase")
def delete_purchase_by_id(request, purchase_id: int):
    """
    Deletes a purchase by its ID.
    Args:
        request: the HTTP request
        purchase_id: the ID of the purchase
    Returns:
        a JSON response with the status of the operation
    """
    purchase = get_purchase_by_id(purchase_id)
    if not purchase:
        return JsonResponse(
            {"status": "error", "message": "Purchase not found"}, status=404
        )
    if purchase["purchaser_user_id"] != request.auth:
        return JsonResponse(
            {"status": "error", "message": "User is not the purchaser"}, status=403
        )
    execute_query(
        Path("purchases/sql/delete_purchase_by_id.sql"),
        {"purchase_id": purchase_id},
    )
    return JsonResponse({}, status=200)


@router.put("/update_purchase/")
def update_purchase_by_id(request, purchase: Purchase):
    """
    Updates a purchase by its ID.
    Args:
        request: the HTTP request
        purchase_id: the ID of the purchase
        purchase: the updated purchase object
    Returns:
        a JSON response with the status of the operation
    """
    purchase_from_db = get_purchase_by_id(purchase.purchase_id)
    if not purchase_from_db:
        return JsonResponse(
            {"status": "error", "message": "Purchase not found"}, status=404
        )
    if not verify_user_in_group(request.auth, purchase_from_db["purchaser_group_id"]):
        return JsonResponse(
            {"status": "error", "message": "You are unauthorized to access this group"},
            status=403,
        )
    if not valid_purchase(purchase):
        return JsonResponse(
            {"status": "error", "message": "Purchase splits do not sum up to total"},
            status=400,
        )
    # delete the old splits
    execute_query(
        Path("purchases/sql/delete_purchase_splits_by_purchase_id.sql"),
        {"purchase_id": purchase.purchase_id},
    )
    # insert the new splits
    split_purchase(purchase, purchase.purchase_id)

    return JsonResponse({}, status=200)
