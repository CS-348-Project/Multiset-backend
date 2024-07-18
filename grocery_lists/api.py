from grocery_lists.models import GroceryList, GroceryListCreate, GroceryListItemCreate, GroceryListUpdate
from grocery_lists.services import add_item_to_grocery_list, create_grocery_list, delete_grocery_list, delete_grocery_list_item, get_grocery_list_by_id, get_grocery_list_items, get_grocery_lists_by_group_id, toggle_grocery_list_item, update_grocery_list
from groups.services import verify_user_in_group
from ninja import Router
from django.http import JsonResponse

router = Router()

@router.get("/")
def get_grocery_lists_handler(request, group_id: int):
    try:
        verify_user_in_group(request.auth, group_id)
        ret = get_grocery_lists_by_group_id(group_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching grocery lists"}, status=500)
    
@router.post("/create")
def add_grocery_list_handler(request, new_grocery_list: GroceryListCreate):
    try:
        verify_user_in_group(request.auth, new_grocery_list.group_id)
        ret = create_grocery_list(new_grocery_list)
        return JsonResponse(ret, status=201)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in saving grocery list"}, status=500)
    
@router.put("/update")
def update_grocery_list_handler(request, grocery_list: GroceryListUpdate):
    try:
        current_grocery_list: GroceryList = get_grocery_list_by_id(grocery_list.id)
        verify_user_in_group(request.auth, current_grocery_list.get("group_id"))
        update_grocery_list(grocery_list)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in updating grocery list"}, status=500)
    
@router.delete("/delete")
def delete_grocery_list_handler(request, id: int):
    try:
        grocery_list: GroceryList = get_grocery_list_by_id(id)
        verify_user_in_group(request.auth, grocery_list.get("group_id"))
        delete_grocery_list(id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in deleting grocery list"}, status=500)
    
@router.post("/add-item")
def add_item_to_grocery_list_handler(request, grocery_list_item: GroceryListItemCreate):
    try:
        grocery_list: GroceryList = get_grocery_list_by_id(grocery_list_item.grocery_list_id)
        verify_user_in_group(request.auth, grocery_list.get("group_id"))
        grocery_list_item.requester_user_id = request.auth
        add_item_to_grocery_list(grocery_list_item)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in adding item to grocery list"}, status=500)
    
@router.get("/items")
def get_grocery_list_items_handler(request, grocery_list_id: int):
    try:
        grocery_list: GroceryList = get_grocery_list_by_id(grocery_list_id)
        verify_user_in_group(request.auth, grocery_list.get("group_id"))
        ret = get_grocery_list_items(grocery_list_id)
        return JsonResponse(ret, safe=False, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in fetching grocery list items"}, status=500)
    
@router.post("/toggle-item")
def toggle_grocery_list_item_handler(request, item_id: int, grocery_list_id: int):
    try:
        grocery_list: GroceryList = get_grocery_list_by_id(grocery_list_id)
        verify_user_in_group(request.auth, grocery_list.get("group_id"))
        toggle_grocery_list_item(item_id, grocery_list_id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in completing grocery list item"}, status=500)
    
@router.delete("/delete-item")
def delete_grocery_list_item_handler(request, item_id: int, grocery_list_id: int):
    try:
        grocery_list: GroceryList = get_grocery_list_by_id(grocery_list_id)
        verify_user_in_group(request.auth, grocery_list.get("group_id"))
        delete_grocery_list_item(item_id, grocery_list_id)
        return JsonResponse({}, status=204)
    except Exception as e:
        return JsonResponse({"status": "error", "message": "Error in deleting grocery list item"}, status=500)

