from ninja import Router
from django.http import JsonResponse

from optimization.services import calculate_handler, flag_handler, toggle_handler

router = Router()


@router.get("/flag")
def flag(request, group_id: int):
    ret = flag_handler(group_id)
    return JsonResponse(ret, status=200)


@router.patch("/toggle")
def toggle(request, group_id: int):
    ret = toggle_handler(group_id)
    return JsonResponse(ret, status=200)


@router.post("/calculate")
def calculate(request, group_id: int):
    return calculate_handler(group_id)
