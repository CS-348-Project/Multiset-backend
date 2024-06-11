/*
Name: add_item_to_grocery_list.sql
Description: adds an item to a grocery list
Usage: {grocery_list_id, member_id, item_name, quantity, notes}
*/
INSERT INTO grocery_list_item (grocery_list_id, member_id, item_name, quantity, notes)
VALUES (%(grocery_list_id)s, %(member_id)s, %(item_name)s, %(quantity)s, %(notes)s)