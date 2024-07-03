/*
Name: toggle_grocery_list_item
Description: Toggles the completion status of a grocery list item
Usage: {id = 1, grocery_list_id = 1}
*/
UPDATE grocery_list_item
SET completed = NOT completed
WHERE id = 1 AND grocery_list_id = 1;