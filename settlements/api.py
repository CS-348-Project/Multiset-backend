from ninja import Router
from django.http import JsonResponse
from .models import SettlementCreate
from .services import find_settlements, save_settlement, find_settlements_between_members

router = Router()

@router.get("/")
def get_settlements(request, member_id: int = None, group_id: int = None):
    try: 
        ret = find_settlements(group_id, member_id)
        return ret
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching settlements"}, status=400)

@router.get("/members")
def get_settlements_between_members(request, member1_id: int, member2_id: int):
    try: 
        ret = find_settlements_between_members(member1_id, member2_id)
        return ret
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching settlements"}, status=400)
        
@router.post("/save")
def add_settlement(request, new_settlement: SettlementCreate):
    if new_settlement.amount <= 0:
        return JsonResponse({"status": "error", "message": "Amount must be greater than 0"}, status=400)
    if new_settlement.sender_id == new_settlement.receiver_id:
        return JsonResponse({"status": "error", "message": "Sender and receiver cannot be the same"}, status=400)
    try:
        save_settlement(new_settlement)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in saving settlement"}, status=400)
