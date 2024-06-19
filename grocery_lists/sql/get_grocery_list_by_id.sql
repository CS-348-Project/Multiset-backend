/*
Name: get_grocery_lists_by_id
Description: Get grocery lists by id
Usage: {id}
*/
SELECT * FROM grocery_list
WHERE id = %(id)s