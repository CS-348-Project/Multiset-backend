/*
Name: update_grocery_list.sql
Description: updates the name of a grocery list
Usage: {id, name}
*/
UPDATE grocery_list
SET name = %(name)s
WHERE grocery_list_id = %(id)s;