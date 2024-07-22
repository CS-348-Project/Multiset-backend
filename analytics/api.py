from groups.services import verify_user_in_group
from ninja import Router
from django.http import JsonResponse
from analytics.services import get_purchase_category_count, get_top_spenders

router = Router()


@router.get("/purchase-categories")
def purchase_category_count_handler(request, group_id: int):
    if (not verify_user_in_group(request.auth, group_id)):
        return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
    return get_purchase_category_count(group_id)


@router.get("/top-spenders")
def top_spenders_handler(request, group_id: int):
    if (not verify_user_in_group(request.auth, group_id)):
        return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
    return get_top_spenders(group_id)
