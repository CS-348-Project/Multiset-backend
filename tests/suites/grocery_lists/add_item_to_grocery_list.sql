/*
Name: add_item_to_grocery_list.sql
Description: adds an item to a grocery list
Usage: {grocery_list_id = 1, requester_user_id = 1, requester_group_id = 1, item_name = "Eggs", quantity = 3, notes = "Costco"}
*/
INSERT INTO grocery_list_item (grocery_list_id, requester_user_id, requester_group_id, item_name, quantity, notes)
VALUES (1, 1, 1, 'Eggs', 3, 'Costco')