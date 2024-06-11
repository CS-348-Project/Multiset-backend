from ninja import Router
from analytics.services import get_purchase_category_count, get_top_spenders

router = Router()


@router.get("/purchase-categories")
def purchase_category_count_handler(request, group_id: int):
    return get_purchase_category_count(group_id)


@router.get("/top-spenders")
def top_spenders_handler(request, group_id: int):
    return get_top_spenders(group_id)
