/*
Name: get_grocery_lists_by_group_id
Description: Get grocery lists by group id
Usage: {group_id = 1}
*/
-- prodorder id;
SELECT * FROM grocery_list
WHERE group_id = 1
ORDER BY grocery_list.id LIMIT 10;
