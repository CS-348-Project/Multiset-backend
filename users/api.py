from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from users.services import get_user

from typing import List, Optional
from .models import User

router = Router()

@router.get("/")
def get_user_handler(request, email: Optional[str] = None, user_id: Optional[int] = None):
    """
    Gets a user by their email or id.
    Args:
        email: the email of the user to retrieve
        user_id: the id of the user to retrieve
    Returns:
        a JSON response with the status of the operation and the user retrieved
    """
    try:
        ret = get_user(email, user_id)
        if len(ret) == 0:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        
        return ret
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
