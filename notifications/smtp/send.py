from pathlib import Path

from multiset.db_utils import execute_query
from notifications.smtp.notif import EmailNotification


def send_email_notifications():
    notif_data = execute_query(
        Path("notifications/sql/get_all_pending.sql"), fetchall=True
    )

    for item in notif_data:
        try:
            count = len(item["notifications"])
        except TypeError:  # no notifications
            continue

        email_address = item["email"]
        name = item["first_name"]

        # make a very simple email
        # might make templates later

        subject = f"{count} new notification{'s' if count > 1 else ''} from Multiset"

        body = f"Hi {name},<br/>You have {count} new Multiset notification{'s' if count > 1 else ''}:<br/><ul>"

        for notif in item["notifications"]:
            body += f"<li>{notif["message"]}</li>"

        body += "</ul>"

        EmailNotification().subject(subject).body(body).recipient(email_address).send()

        # mark as sent
        execute_query(
            Path("notifications/sql/mark_all_as_sent.sql"),
            {"user_id": item["id"]}
        )


