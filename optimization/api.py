from ninja import Router
from django.http import JsonResponse

from optimization.utils import _verify_group
from optimization.services import calculate, flag, toggle

router = Router()


@router.get("/flag")
@_verify_group
def flag_handler(request, group_id: int):
    ret = flag(group_id)
    return JsonResponse(ret, status=200)


@router.patch("/toggle")
@_verify_group
def toggle_handler(request, group_id: int):
    ret = toggle(group_id)
    return JsonResponse(ret, status=200)


@router.post("/calculate")
@_verify_group
def calculate_handler(request, group_id: int):
    return calculate(group_id)
