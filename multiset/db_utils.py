import os
from typing import List
from django.conf import settings
from django.db import connection
from pathlib import Path


def _load_sql(filepath: Path):
    """Utility function to load SQL from a file."""
    filename = settings.BASE_DIR / filepath
    with open(filename, 'r') as file:
        return file.read()


def execute_query(
    filepath: Path,
    params: List = None,
    fetchone: bool = False,
    fetchall: bool = False,
):
    """Executes a SQL query directly with optional parameter substitution."""
    sql = _load_sql(filepath)
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return None
