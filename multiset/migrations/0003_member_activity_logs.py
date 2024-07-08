from django.db import migrations
from pathlib import Path

from multiset.db_utils import execute_query

def sql_operation(filepath: Path):
    def inner(apps, schema_editor):
        execute_query(filepath)

    return migrations.RunPython(inner)

class Migration(migrations.Migration):
  dependencies = [("multiset", "0001_db_setup"), ("multiset", "0002_add_indexes")]
  
  operations = [
    sql_operation(Path("member_activity_logs/sql/triggers/member_triggers.sql")),
    sql_operation(Path("member_activity_logs/sql/triggers/purchase_triggers.sql")),
    sql_operation(Path("member_activity_logs/sql/triggers/settlement_triggers.sql")),
    sql_operation(Path("member_activity_logs/sql/triggers/grocery_list_triggers.sql")),
  ]