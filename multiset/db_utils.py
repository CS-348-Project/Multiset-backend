from typing import List
from django.conf import settings
from django.db import connection, Error
from functools import wraps
from pathlib import Path
from django.http import JsonResponse
from optimization.services import calculate
from purchases.models import Purchase
from settlements.models import SettlementCreate


def _load_sql(filepath: Path):
    """Utility function to load SQL from a file."""
    filename = settings.BASE_DIR / filepath
    with open(filename, "r") as file:
        return file.read()


def dictfetchone(cursor):
    "Return one row from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def execute_query(
    filepath: Path,
    params: dict = None,
    fetchone: bool = False,
    fetchall: bool = False,
):
    """Executes a SQL query directly with optional parameter substitution."""
    sql = _load_sql(filepath)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            if cursor.description is None:
                return None
            if fetchone:
                if cursor.rowcount == 0:
                    return {}
                return dictfetchone(cursor)
            if fetchall:
                if cursor.rowcount == 0:
                    return []
                return dictfetchall(cursor)
            return None
    except Error as e:
        print(f"An error occurred: {e}")
        return None


def _verify_group(func):
    """
    Decorator to verify that the given group_id is valid
    and that the user is a member of the group
    """

    def wrapper(request, group_id: int):
        # check if group_id is provided
        if not group_id:
            return JsonResponse({"error": "group_id is required"}, status=400)

        # check if group_id is valid (i.e. user is a member of the group)
        groups = execute_query(
            "groups/sql/get_groups_by_user_id.sql",
            {"user_id": request.auth},
            fetchall=True,
        )

        if group_id not in [group["id"] for group in groups]:
            # this could also be a 404 if no group with that id exists
            # but this also works
            return JsonResponse(
                {"error": f"User is not a member of a group with id {group_id}"},
                status=403,
            )

        # call the original function
        return func(request, group_id)

    return wrapper


def update_debts(func):
    """
    Decorator to update debts after a change in the database
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # make sure the function can be used with this decorator
        if not (
            "purchase" in kwargs
            or "new_settlement" in kwargs
            or "group_id" in kwargs
            or (len(kwargs) == 1 and "group_id" in kwargs[list(kwargs.keys())[0]])
        ):

            # if it can't, return an error immediately
            return JsonResponse(
                {"error": f"Cannot use update_debts decorator on {func.__name__}"},
                status=500,
            )

        # call the original function
        response = func(*args, **kwargs)

        # if the response is an error, return it and don't update debts
        if response.status_code > 299 or response.status_code < 200:
            return response

        if "group_id" in kwargs:
            group_id = kwargs["group_id"]
            calculate(group_id)

        # check if kwargs has a purchase object
        elif "purchase" in kwargs:
            purchase: Purchase = kwargs["purchase"]
            calculate(purchase.group_id)

        # check if kwargs has a settlement object
        elif "new_settlement" in kwargs:
            settlement: SettlementCreate = kwargs["new_settlement"]
            calculate(settlement.group_id)

        # otherwise, get the group_id from the first kwarg (len(kwargs) == 1)
        else:
            group_id = kwargs[list(kwargs.keys())[0]]["group_id"]
            calculate(group_id)

        # return the original response
        return response

    return wrapper
