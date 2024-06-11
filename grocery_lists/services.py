from grocery_lists.models import GroceryListCreate
from multiset.db_utils import execute_query
from purchases.models import Purchase
from django.http import JsonResponse
from pathlib import Path

def get_grocery_lists_by_group_id(group_id: int):
    grocery_lists = execute_query(
        Path("grocery_lists/sql/get_grocery_lists_by_group_id.sql"),
        {"group_id": group_id},
        fetchall=True)
    return grocery_lists
  
def create_grocery_list(new_grocery_list: GroceryListCreate):
    execute_query(
        Path("grocery_lists/sql/create_grocery_list.sql"),
        {
            "group_id": new_grocery_list.group_id,
            "name": new_grocery_list.name,
        },
    )
    return True