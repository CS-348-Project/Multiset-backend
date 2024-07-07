from django.db import migrations
from pathlib import Path

from multiset.db_utils import execute_sql


def sql_operation(filepath: Path):
    def inner(apps, schema_editor):
        execute_sql(filepath)

    return migrations.RunPython(inner)


class Migration(migrations.Migration):
    dependencies = [("multiset", "0002_add_indexes")]

    operations = [
        sql_operation(Path("notifications/sql/triggers/new_group.sql")),
        sql_operation(Path("notifications/sql/triggers/new_list.sql")),
    ]
