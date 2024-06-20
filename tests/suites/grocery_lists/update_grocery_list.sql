/*
Name: update_grocery_list.sql
Description: updates the name of a grocery list
Usage: {id = 1, name = "Another Party"}
*/
UPDATE grocery_list
SET name = 'Another Party'
WHERE id = 1;