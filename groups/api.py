from ninja import Router
from django.http import JsonResponse
from multiset.db_utils import execute_query
from pathlib import Path
from groups.services import get_group, create_group, update_group, delete_group, verify_user_in_group

from typing import List, Optional
from .models import Group, GroupSkeleton

router = Router()

@router.get("/")
def get_group_handler(request, group_id: Optional[int] = None, detailed: Optional[bool] = False):
    """
    Gets a group by its id.
    Args:
        group_id: the id of the group to be retrieved
        user_id: the id of the user to get the groups for
    Returns:
        a JSON response with the status of the operation and the group or groups retrieved
    """
    try:
        ret = get_group(group_id, request.auth, detailed)
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
        ret = create_group(group, user_ids)
        return JsonResponse(ret, status=201)
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

@router.get("/other-members")
def get_other_group_members_handler(request, group_id: int):
    """
    Gets the other members of a group.
    Args:
        group_id: the id of the group to get the members of
    Returns:
        a JSON response with the status of the operation and the list of members
    """
    try:
        verify_user_in_group(request.auth, group_id)
        group = get_group(group_id, detailed=True)
        if not group:
            return JsonResponse({"status": "error", "message": "Group not found"}, status=404)
        other_members = [user for user in group["users"] if user["id"] != request.auth]
        return JsonResponse(other_members, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)