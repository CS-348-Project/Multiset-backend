/*
Name: delete_grocery_list.sql
Description: deletes a grocery list by id
Usage: {id}
*/
DELETE FROM grocery_list WHERE id = %(id)s;