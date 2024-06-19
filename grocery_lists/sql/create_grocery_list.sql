/*
Name: create_grocery_list.sql
Description: creates a new grocery list
Usage: {group_id, name}
*/
INSERT INTO grocery_list (group_id, name) 
VALUES (%(group_id)s, %(name)s) 
RETURNING id;