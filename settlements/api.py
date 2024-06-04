from ninja import Router

router = Router()

@router.get("/items")
def list_items(request):
    return "hi"