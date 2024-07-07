from typing import List
from django.conf import settings
from django.db import connection, Error
from pathlib import Path
from django.http import JsonResponse

def _load_sql(filepath: Path):
    """Utility function to load SQL from a file."""
    filename = settings.BASE_DIR / filepath
    with open(filename, 'r') as file:
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
