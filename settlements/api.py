from ninja import Router
from django.http import JsonResponse
from .models import Settlement
from .services import find_settlements, save_settlement, find_settlements_between_members

router = Router()

@router.get("/")
def get_settlements(request, member_id: int = None, group_id: int = None):
    return find_settlements(group_id=group_id, member_id=member_id)

@router.get("/members")
def get_settlements_between_members(request, member1_id: int, member2_id: int):
    return find_settlements_between_members(member1_id, member2_id)

@router.post("/save")
def add_settlement(request, new_settlement: Settlement):
    if (save_settlement(new_settlement)):
        return JsonResponse({"success": True})