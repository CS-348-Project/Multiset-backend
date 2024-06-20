/*
Name: delete_grocery_list_item.sql
Description: Deletes a grocery list item
Usage: {id, grocery_list_id}
*/
DELETE FROM grocery_list_item
WHERE id = %(id)s AND grocery_list_id = %(grocery_list_id)s