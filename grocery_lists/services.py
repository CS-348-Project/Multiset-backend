from typing import List
from grocery_lists.models import GroceryListCreate, GroceryListItemCreate, GroceryListUpdate
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
    new_grocery_list_id = execute_query(
        Path("grocery_lists/sql/create_grocery_list.sql"),
        {
            "group_id": new_grocery_list.group_id,
            "name": new_grocery_list.name,
        },
    )
    return new_grocery_list_id

def update_grocery_list(grocery_list: GroceryListUpdate):
    execute_query(
        Path("grocery_lists/sql/update_grocery_list.sql"),
        {
            "id": grocery_list.id,
            "name": grocery_list.name,
        },
    )
    return True

def delete_grocery_list(id: int):
    execute_query(
        Path("grocery_lists/sql/delete_grocery_list.sql"),
        {"id": id},
    )
    return True

def add_item_to_grocery_list(grocery_list_id: int, grocery_list_item: GroceryListItemCreate):
    execute_query(
        Path("grocery_lists/sql/add_item_to_grocery_list.sql"),
        {
            "grocery_list_id": grocery_list_id,
            "member_id": grocery_list_item.member_id,
            "item_name": grocery_list_item.item_name,
            "quantity": grocery_list_item.quantity,
            "notes": grocery_list_item.notes,
        },
    )
    return True

def get_grocery_list_items(grocery_list_id: int):
    grocery_list_items = execute_query(
        Path("grocery_lists/sql/get_grocery_list_items.sql"),
        {"grocery_list_id": grocery_list_id},
        fetchall=True)
    return grocery_list_items

def toggle_grocery_list_item(item_id: int):
    execute_query(
        Path("grocery_lists/sql/toggle_grocery_list_item.sql"),
        {
            "id": item_id,
        },
    )
    return True

def delete_grocery_list_item(item_id: int):
    execute_query(
        Path("grocery_lists/sql/delete_grocery_list_item.sql"),
        {
            "id": item_id,
        },
    )
    return True