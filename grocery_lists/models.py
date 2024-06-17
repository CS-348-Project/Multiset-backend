from datetime import datetime
from typing import List
from ninja import Schema

class GroceryListCreate(Schema):
  group_id: int
  name: str
  
class GroceryListUpdate(Schema):
  id: int
  name: str

class GroceryList(Schema):
  id: int
  group_id: int
  name: str
  created_at: datetime
  
class GroceryListMemberInfo(Schema):
  member_id: int
  first_name: str
  last_name: str
  
class GroceryListItem(Schema):
  id: int
  member: GroceryListMemberInfo
  item_name: str
  quantity: int
  completed: bool
  notes: str
  
class GroceryListItemCreate(Schema):
  grocery_list_id: int
  requester_user_id: int
  requester_group_id: int
  item_name: str
  quantity: int
  notes: str
  
class GroceryListWithItems(Schema):
  id: int
  group_id: int
  name: str
  created_at: datetime
  items: List[GroceryListItem]