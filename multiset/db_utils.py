from typing import List
from django.conf import settings
from django.db import connection, Error
from pathlib import Path


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
