from datetime import datetime
import jwt
from multiset import settings
from multiset.db_utils import execute_query

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"


def get_associated_user_id(token: str) -> bool:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    res = execute_query(
        "auth/sql/user_id_exists.sql", {"user_id": user_id}, fetchone=True
    )
    if res["id"]:
        return res["id"]
    else:
        return None


def find_id_from_email(email: str) -> int:
    res = execute_query("auth/sql/email_exists.sql", {"email": email}, fetchone=True)
    return res.get("id")


def create_new_user(email: str, first_name: str, last_name: str, google_id: str) -> int:
    res = execute_query(
        "auth/sql/create_new_user.sql",
        {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "google_id": google_id,
        },
        fetchone=True,
    )
    return res["id"]
