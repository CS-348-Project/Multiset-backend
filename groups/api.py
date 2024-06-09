from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from groups.services import get_group, create_group, update_group, delete_group

from typing import List, Optional
from .models import Group, GroupSkeleton

router = Router()

@router.get("/", response=List[Group])
def get_group_handler(request, group_id: Optional[int] = None, user_id: Optional[int] = None):
    """
    Gets a group by its id.
    Args:
        group_id: the id of the group to be retrieved
        user_id: the id of the user to get the groups for
    Returns:
        a JSON response with the status of the operation and the group or groups retrieved
    """
    try:
        ret = get_group(group_id, user_id)
        return ret
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@router.post("/create")
def create_group_handler(request, group: GroupSkeleton, user_ids: List[int] = []):
    """
    Creates a new group in the database.
    Args:
        group: the group to be created along and the user that created it
    Returns:
        a JSON response with the status of the operation and the created group id
    """
    
    if len(user_ids) == 0:
        return JsonResponse({"status": "error", "message": "No users provided for group"}, status=400)
    try:
        create_group(group, user_ids)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@router.put("/update")
def update_group_handler(request, group: Group):
    """
    Updates a group in the database.
    Args:
        group: the group to be updated
    Returns:
        a JSON response with the status of the operation
    """
    try:
        update_group(group)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@router.post("/delete")
def delete_group_handler(request, group_id: int):
    """
    Deletes a group from the database.
    Args:
        group_id: the id of the group to be deleted
    Returns:
        a JSON response with the status of the operation
    """
    try:
        delete_group(group_id)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

