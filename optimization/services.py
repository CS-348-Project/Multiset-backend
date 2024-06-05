from multiset.db_utils import execute_query
from purchases.models import Purchase
from django.http import JsonResponse
from pathlib import Path


def test():
    q = execute_query(
        "optimization/sql/get_group_balances.sql",
        {
            "group_id": 3,
        },
        fetchall=True,
    )

    return JsonResponse(q, safe=False)
