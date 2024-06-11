/*
Name: get_grocery_list_items.sql
Description: Get grocery list items by grocery list id
Usage: {grocery_list_id}
*/
SELECT * FROM grocery_list_item
WHERE grocery_list_id = %(grocery_list_id)s