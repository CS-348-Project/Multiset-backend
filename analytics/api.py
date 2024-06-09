from ninja import Router
from analytics.services import get_purchase_category_count

router = Router()


@router.get("/purchase-categories")
def root(request, group_id: int):
    return get_purchase_category_count(group_id)
