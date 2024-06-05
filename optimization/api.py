from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path

from optimization.services import test as test_service

router = Router()


@router.get("/test")
def test(request):
    return test_service()
