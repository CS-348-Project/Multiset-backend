/*
Name: get_purchases_by_id.sql
Description: Get purchase info based on purchase id
Usage: {purchase_id = 1}
Return: {id, category, name, total_cost, created_at}
*/
-- prodorder id
SELECT id, category, name, total_cost, created_at
FROM purchase p
WHERE id = 1
ORDER BY id
LIMIT 10;
