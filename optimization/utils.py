from django.http import JsonResponse

from multiset.db_utils import execute_query


def _verify_group(func):
    """
    Decorator to verify that the given group_id is valid
    and that the user is a member of the group
    """

    def wrapper(request, group_id: int):
        # check if group_id is provided
        if not group_id:
            return JsonResponse({"error": "group_id is required"}, status=400)

        # check if group_id is valid (i.e. user is a member of the group)
        groups = execute_query(
            "groups/sql/get_groups_by_user_id.sql",
            {"user_id": request.auth},
            fetchall=True,
        )

        if group_id not in [group["id"] for group in groups]:
            # this could also be a 404 if no group with that id exists
            # but this also works
            return JsonResponse(
                {"error": f"User is not a member of a group with id {group_id}"},
                status=403,
            )

        # call the original function
        return func(request, group_id)

    return wrapper
