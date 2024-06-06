from ninja import Router
from django.http import JsonResponse

from optimization.models import GroupId
from optimization.services import calculate_transfers

router = Router()


@router.post("/calculate")
def test(request, gid: GroupId):
    solution = calculate_transfers(gid)

    if solution:
        return JsonResponse(solution, safe=False, status=200)

    return JsonResponse({"status": "error"}, status=500)
