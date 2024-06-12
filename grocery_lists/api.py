from grocery_lists.models import GroceryListCreate, GroceryListItemCreate, GroceryListUpdate
from grocery_lists.services import add_item_to_grocery_list, create_grocery_list, delete_grocery_list, delete_grocery_list_item, get_grocery_list_items, get_grocery_lists_by_group_id, toggle_grocery_list_item, update_grocery_list
from ninja import Router
from django.http import JsonResponse

router = Router()

@router.get("/")
def get_grocery_lists_handler(request, group_id: int):
    try:
        ret = get_grocery_lists_by_group_id(group_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching grocery lists"}, status=500)
    
@router.post("/create")
def add_grocery_list_handler(request, new_grocery_list: GroceryListCreate):
    try:
        ret = create_grocery_list(new_grocery_list)
        return JsonResponse({"id": ret}, status=201)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in saving grocery list"}, status=500)
    
@router.put("/update")
def update_grocery_list_handler(request, grocery_list: GroceryListUpdate):
    try:
        update_grocery_list(grocery_list)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in updating grocery list"}, status=500)
    
@router.delete("/delete")
def delete_grocery_list_handler(request, id: int):
    try:
        delete_grocery_list(id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in deleting grocery list"}, status=500)
    
@router.post("/add-item")
def add_item_to_grocery_list_handler(request, grocery_list_item: GroceryListItemCreate):
    try:
        add_item_to_grocery_list(grocery_list_item)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in adding item to grocery list"}, status=500)
    
@router.get("/items")
def get_grocery_list_items_handler(request, grocery_list_id: int):
    try:
        ret = get_grocery_list_items(grocery_list_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching grocery list items"}, status=500)
    
@router.post("/toggle-item")
def toggle_grocery_list_item_handler(request, item_id: int):
    try:
        toggle_grocery_list_item(item_id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in completing grocery list item"}, status=500)
    
@router.delete("/delete-item")
def delete_grocery_list_item_handler(request, item_id: int):
    try:
        delete_grocery_list_item(item_id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in deleting grocery list item"}, status=500)