/*
Name: new_purchase.sql
Description: Insert a new row into the purchase table
Usage: {name=”Apples”, category=”groceries”, group_id = 2, total_cost=500, purchaser=1}
Return: {id}
*/

INSERT INTO purchase (name, category, purchaser_group_id, total_cost, purchaser_user_id)
VALUES ('Apples', 'groceries', 1, 500, 1) RETURNING id