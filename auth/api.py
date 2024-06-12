from multiset import settings
from ninja import Router
import requests
from ninja import Schema
from auth.services import create_new_user, user_already_registered
import jwt
from datetime import datetime, timedelta

router = Router()


class TokenModel(Schema):
    token: str


@router.post("/google", auth=None)
def callback_handler(request, token: TokenModel):

    response = requests.get(
        f"https://oauth2.googleapis.com/tokeninfo?id_token={token.token}"
    )
    if response.status_code == 200:
        user_info = response.json()

        email = user_info.get("email")
        first_name = user_info.get("given_name")
        last_name = user_info.get("family_name")

        if user_already_registered(email):
            return {"success": True}

        new_user_id = create_new_user(email, first_name, last_name)

        # create new jwt token which is returned to the frontend to be stored in the cache
        payload = {
            "email": email,
            "user_id": new_user_id,
            "google_id": user_info.get("sub"),
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return {"token": jwt_token}
    else:
        return {"error": "Invalid token"}
