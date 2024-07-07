from django.conf import settings
from email.mime.text import MIMEText
import os
from smtplib import SMTP
from typing import Optional


class EmailNotification:
    def __init__(self):
        self.restart_session()
        self._login()
        self._subject: Optional[str] = None
        self._recipient: Optional[str] = None
        self._body: Optional[str] = None
        self._subtype: Optional[str] = None

    def subject(self, subject):
        self._subject = subject
        return self

    def recipient(self, recipient):
        self._recipient = recipient
        return self

    def body(self, body, subtype="html"):
        self._body = body
        self._subtype = subtype
        return self

    def send(self):
        assert self._subject is not None, "Subject is required"
        assert self._recipient is not None, "Recipient is required"
        assert self._body is not None, "Body is required"
        assert self._subtype is not None, "Subtype is required"

        message = MIMEText(self._body, self._subtype)

        message["Subject"] = self._subject
        message["From"] = self._username
        message["To"] = self._recipient

        self._session.send_message(message)
        return self

    def restart_session(self):
        self._session = SMTP("smtp.gmail.com", 587)
        self._session.starttls()

        return self

    def _login(self):
        self._session.login(os.getenv("SMTP_EMAIL"), os.getenv("SMTP_PASSWORD"))
        self._username = os.getenv("SMTP_EMAIL")
        return self
