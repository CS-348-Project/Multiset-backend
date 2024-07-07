from groups.services import verify_user_in_group
from member_activity_logs.services import get_member_activity_logs_by_group_id
from ninja import Router
from django.http import JsonResponse

router = Router()

@router.get("/")
def get_member_activity_logs_handler(request, group_id: int):
    try:
        verify_user_in_group(request.auth, group_id)
        ret = get_member_activity_logs_by_group_id(group_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching member activity logs"}, status=500)