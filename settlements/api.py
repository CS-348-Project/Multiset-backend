from ninja import Router
from .services import get_settlements

router = Router()

@router.get("/items")
def list_items(request):
    return "hi"

@router.get("/")
def list_items(request):
    return get_settlements()