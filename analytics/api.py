from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from purchases.models import Purchase
from analytics.services import get_purchase_category_count

router = Router()


@router.get("/purchase-categories")
def root(request, group_id: int):
    return get_purchase_category_count(group_id)
