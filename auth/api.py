from multiset import settings
from ninja import Router
import requests
from ninja import Schema
from auth.services import create_new_user, find_id_from_email
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
        google_id = user_info.get("sub")

        user_id = find_id_from_email(email)
        if not user_id:
            user_id = create_new_user(email, first_name, last_name, google_id)

        # create new jwt token which is returned to the frontend to be stored in the cache
        # TODO: have a look at the expiration time of the token
        payload = {
            "email": email,
            "user_id": user_id,
            "google_id": google_id,
        }
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        return {"token": jwt_token}
    else:
        return {"error": "Invalid token"}
