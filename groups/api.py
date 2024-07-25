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
        if (group_id and not verify_user_in_group(request.auth, group_id)):
            return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
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

@router.delete("/delete")
def delete_group_handler(request, group_id: int):
    """
    Deletes a group from the database.
    Args:
        group_id: the id of the group to be deleted
    Returns:
        a JSON response with the status of the operation
    """
    try:
        if (group_id and not verify_user_in_group(request.auth, group_id)):
            return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
        delete_group(group_id)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@router.get("/members")
def get_group_members_handler(request, group_id: int, exclude_current_user: Optional[bool] = False):
    """
    Gets the other members of a group.
    Args:
        group_id: the id of the group to get the members of
        exclude_current_user: whether to exclude the current user from the list of members
    Returns:
        a JSON response with the status of the operation and the list of members
    """
    try:
        if (not verify_user_in_group(request.auth, group_id)):
            return JsonResponse({"status": "error", "message": "You are unauthorized to access this group"}, status=403)
        group = get_group(group_id, detailed=True)
        if not group:
            return JsonResponse({"status": "error", "message": "Group not found"}, status=404)
        if exclude_current_user:
            members = [user for user in group["users"] if user["id"] != request.auth]
        else:
            members = group["users"]
        return JsonResponse(members, safe=False)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)