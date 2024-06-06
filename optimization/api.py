from ninja import Router
from django.http import JsonResponse

from optimization.models import GroupId
from optimization.services import calculate_transfers

router = Router()


@router.post("/calculate")
def test(request, gid: GroupId):
    return calculate_transfers(gid)
