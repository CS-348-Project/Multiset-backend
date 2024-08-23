from django.db import migrations
from pathlib import Path

from multiset.db_utils import execute_query


def sql_operation(filepath: Path):
    def inner(apps, schema_editor):
        execute_query(filepath)

    return migrations.RunPython(inner)


class Migration(migrations.Migration):
    dependencies = [
        ("multiset", "0001_db_setup"),
        ("multiset", "0002_add_indexes"),
        ("multiset", "0003_notifications"),
        ("multiset", "0004_member_activity_logs"),
        ("multiset", "0005_member_activity_logs_safety_check"),
    ]

    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE multiset_group ADD share_code VARCHAR(255) NOT NULL DEFAULT '';
            CREATE INDEX multiset_group_share_code ON multiset_group (share_code);      
        """
        )
    ]
