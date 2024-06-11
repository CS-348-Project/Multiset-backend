/*
Name: get_grocery_list_items.sql
Description: Get grocery list items by grocery list id
Usage: {grocery_list_id}
*/
SELECT 
  grocery_list_item.id, 
  grocery_list_item.item_name,
  grocery_list_item.quantity,
  grocery_list_item.completed,
  grocery_list_item.notes,
  grocery_list_item.member_id,
  multiset_user.first_name AS member_first_name,
  multiset_user.last_name AS member_last_name
FROM grocery_list_item
JOIN member ON member.id = grocery_list_item.member_id
JOIN multiset_user ON member.user_id = multiset_user.id
WHERE grocery_list_id = %(grocery_list_id)s