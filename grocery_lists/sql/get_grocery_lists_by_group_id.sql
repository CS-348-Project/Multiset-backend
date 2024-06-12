/*
Name: get_grocery_lists_by_group_id
Description: Get grocery lists by group id
Usage: {group_id}
*/
SELECT * FROM grocery_list
WHERE group_id = %(group_id)s