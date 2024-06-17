from groups.services import verify_user_in_group
from ninja import Router
from django.http import JsonResponse
from .models import SettlementCreate
from .services import find_settlements, save_settlement, find_settlements_between_members

router = Router()

@router.get("/")
def get_settlements_handler(request, group_id: int, member_user_id: int = None):
    try: 
        if (not verify_user_in_group(request.auth, group_id)):
            return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
        ret = find_settlements(group_id, member_user_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching settlements"}, status=400)

@router.get("/members")
def get_settlements_between_members_handler(request, member1_user_id: int, member2_user_id: int, group_id: int):
    try: 
        if (not verify_user_in_group(request.auth, group_id)):
            return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
        ret = find_settlements_between_members(member1_user_id, member2_user_id, group_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching settlements"}, status=400)
        
@router.post("/create")
def add_settlement_handler(request, new_settlement: SettlementCreate):
    if (not verify_user_in_group(request.auth, new_settlement.group_id)):
        return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
    if (not request.auth == new_settlement.sender_user_id):
        return JsonResponse({"status": "error", "message": "You are unauthorized to create a settlement on behalf of another user"}, status=403)
    if new_settlement.amount <= 0:
        return JsonResponse({"status": "error", "message": "Amount must be greater than 0"}, status=400)
    if new_settlement.sender_user_id == new_settlement.receiver_user_id:
        return JsonResponse({"status": "error", "message": "Sender and receiver cannot be the same"}, status=400)
    try:
        save_settlement(new_settlement)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in saving settlement"}, status=400)
