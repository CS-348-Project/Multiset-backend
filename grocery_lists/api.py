from grocery_lists.models import GroceryListCreate
from grocery_lists.services import get_grocery_lists_by_group_id
from ninja import Router
from django.http import JsonResponse

router = Router()

@router.get("/")
def get_grocery_lists_handler(request, group_id: int):
    try:
        ret = get_grocery_lists_by_group_id()
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching grocery lists"}, status=400)
    
@router.post("/create")
def add_grocery_list_handler(request, new_grocery_list: GroceryListCreate):
    try:
        save_grocery_list(new_grocery_list)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in saving grocery list"}, status=400)