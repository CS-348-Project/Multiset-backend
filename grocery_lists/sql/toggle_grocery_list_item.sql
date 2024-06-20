/*
Name: toggle_grocery_list_item
Description: Toggles the completion status of a grocery list item
Usage: {id, grocery_list_id}
*/
UPDATE grocery_list_item
SET completed = NOT completed
WHERE id = %(id)s AND grocery_list_id = %(grocery_list_id)s