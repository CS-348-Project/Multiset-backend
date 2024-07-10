/*
Name: new_purchase.sql
Description: Insert a new row into the purchase table
Usage: [name, category, group_id, total_cost, purchaser]
Return: {id}
*/

INSERT INTO purchase (name, category, purchaser_group_id, total_cost, purchaser_user_id)
VALUES ('Apples', 'Groceries', 1, 1000, 1) RETURNING id