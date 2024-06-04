/*
Name: new_purchase.sql
Description: Insert a new row into the purchase table
Usage: [name, category, group_id, total_cost, purchaser]
Return: {id}
*/

INSERT INTO purchase (name, category, group_id, total_cost, purchaser)
VALUES (%(name)s, %(category)s, %(group_id)s, %(total_cost)s, %(purchaser)s) RETURNING id