/*
Name: add_item_to_grocery_list.sql
Description: adds an item to a grocery list
Usage: {grocery_list_id, requester_user_id, requester_group_id, item_name, quantity, notes}
*/
INSERT INTO grocery_list_item (grocery_list_id, requester_user_id, requester_group_id, item_name, quantity, notes)
VALUES (%(grocery_list_id)s, %(requester_user_id)s, %(requester_group_id)s, %(item_name)s, %(quantity)s, %(notes)s)