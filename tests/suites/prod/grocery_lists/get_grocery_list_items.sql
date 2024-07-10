/*
Name: get_grocery_list_items.sql
Description: Get grocery list items by grocery list id
Usage: {grocery_list_id = 1}
*/
SELECT 
  grocery_list_item.id,
  grocery_list_item.item_name,
  grocery_list_item.quantity,
  grocery_list_item.notes,
  grocery_list_item.completed,
  json_build_object(
    'user_id', grocery_list_item.requester_user_id,
    'group_id', grocery_list_item.requester_group_id,
    'first_name', multiset_user.first_name, 
    'last_name', multiset_user.last_name
  ) AS member
FROM grocery_list_item
JOIN multiset_user ON grocery_list_item.requester_user_id = multiset_user.id
WHERE grocery_list_item.grocery_list_id = 1
ORDER BY grocery_list_item.id LIMIT 10;
