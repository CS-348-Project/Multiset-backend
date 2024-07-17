/*
Name: get_purchases_by_id.sql
Description: Get purchase info based on purchase id
Usage: {purchase_id}
Return: {id, category, name, total_cost, created_at}
*/

SELECT id, category, name, total_cost, created_at
FROM purchase p
WHERE id = %(purchase_id)s
