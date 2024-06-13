/*
Name: delete_grocery_list_item.sql
Description: Deletes a grocery list item
Usage: {id}
*/
DELETE FROM grocery_list_item
WHERE id = %(id)s;