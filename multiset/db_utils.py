import os
from django.conf import settings
from django.db import connection

def load_sql(filepath):
    """Utility function to load SQL from a file."""
    filename = os.path.join(settings.BASE_DIR, *filepath)
    with open(filename, 'r') as file:
        return file.read()

def execute_query(filepath, params=None, fetchone=False, fetchall=False):
    """Executes a SQL query directly with optional parameter substitution."""
    sql = load_sql(filepath)
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        if fetchone:
            return cursor.fetchone()
        if fetchall:
            return cursor.fetchall()
        return None