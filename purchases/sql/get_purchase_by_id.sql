/*
Name: get_purchases_by_id.sql
Description: Get purchase info based on purchase id
Usage: {purchase_id}
Return: {id, category, name, total_cost, created_at, purchase_user_id}
*/

SELECT id, category, name, total_cost, created_at, purchaser_user_id
FROM purchase p
WHERE id = %(purchase_id)s
