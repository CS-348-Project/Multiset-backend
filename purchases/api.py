from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from purchases.models import Purchase
from purchases.services import new_purchase, split_purchase, valid_purchase

router = Router()


@router.post("/new-purchase")
def create_new_purchase(request, purchase: Purchase):
    """
    Creates a new purchase and its splits in the database.
    Args:
        purchase: the purchase object to be created and a list of purchase splits
    Returns:
        a JSON response with the status of the operation
    """
    if not valid_purchase(purchase):
        return JsonResponse({"error": "The purchase is not valid!"})
    created_purchase = new_purchase(purchase)
    new_purchase_id = created_purchase["id"]
    split_purchase(purchase, new_purchase_id)

    return JsonResponse({"status": "success"})
