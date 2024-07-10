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
        # this should go into the other migrations eventually but having it separate
        # means that it will properly be applied if the db persists for now
        migrations.RunSQL(
            """
            CREATE TABLE notification (
              id SERIAL,
              user_id INT NOT NULL REFERENCES multiset_user(id) ON DELETE CASCADE,
              message VARCHAR(255) NOT NULL,
              read BOOLEAN NOT NULL DEFAULT FALSE,
              email_sent BOOLEAN NOT NULL DEFAULT FALSE,
              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
              PRIMARY KEY (id, user_id)
            );

            CREATE INDEX notification_user_id_idx ON notification (user_id);
            """
        ),
        sql_operation(Path("notifications/sql/triggers/new_group.sql")),
        sql_operation(Path("notifications/sql/triggers/new_list.sql")),
        sql_operation(Path("notifications/sql/triggers/new_purchase.sql")),
        sql_operation(Path("notifications/sql/triggers/new_settlement.sql")),
    ]
