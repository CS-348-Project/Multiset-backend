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


def user_already_registered(email: str) -> bool:
    # TODO: Implement me
    print("Checking if user already registered")
    return False


def create_new_user(email: str, first_name: str, last_name: str) -> int:
    print("Creating new user")
    # get the user id from the database after creating
    return 1
