from django.http import JsonResponse
from ninja import Router

from notifications.services import (
    get_notifications,
    read_notifications,
    delete_notifications,
)

router = Router()


@router.get("/")
def get_notifications_handler(request):
    """
    Get all notifications for the authenticated user.
    """
    return get_notifications(request.auth)


@router.patch("/read")
def read_notifications_handler(request):
    """
    Read all notifications for the authenticated user.
    """
    read_notifications(request.auth)
    return JsonResponse({}, status=204)


@router.delete("/")
def delete_notifications_handler(request):
    """
    Delete all notifications for the authenticated user.
    """
    delete_notifications(request.auth)
    return JsonResponse({}, status=204)
