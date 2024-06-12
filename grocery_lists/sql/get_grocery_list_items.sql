/*
Name: get_grocery_list_items.sql
Description: Get grocery list items by grocery list id
Usage: {grocery_list_id}
*/
SELECT 
  grocery_list_item.*,
  json_build_object(
    'first_name', multiset_user.first_name, 
    'last_name', multiset_user.last_name
  ) AS member
FROM grocery_list_item
JOIN member ON member.id = grocery_list_item.member_id
JOIN multiset_user ON member.user_id = multiset_user.id
WHERE grocery_list_id = %(grocery_list_id)s