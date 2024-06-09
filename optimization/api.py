from ninja import Router
from django.http import JsonResponse

from optimization.services import calculate_transfers

router = Router()


@router.post("/calculate")
def calculate(request, group_id: int):
    return calculate_transfers(group_id)
