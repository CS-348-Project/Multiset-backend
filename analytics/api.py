from groups.services import verify_user_in_group
from ninja import Router
from analytics.services import get_purchase_category_count, get_top_spenders
from django.http import JsonResponse

router = Router()


@router.get("/purchase-categories")
def purchase_category_count_handler(request, group_id: int):
    try:
        verify_user_in_group(request.auth, group_id)
        return get_purchase_category_count(group_id)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching purchase categories"}, status=500)


@router.get("/top-spenders")
def top_spenders_handler(request, group_id: int):
    try:
        verify_user_in_group(request.auth, group_id)
        return get_top_spenders(group_id)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching top spenders"}, status=500)
