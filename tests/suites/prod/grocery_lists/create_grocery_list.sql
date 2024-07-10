/*
Name: create_grocery_list.sql
Description: creates a new grocery list
Usage: {group_id = 1, name = "Party Night"}
*/
INSERT INTO grocery_list (group_id, name) 
VALUES (1, 'Party Night') 
RETURNING id;