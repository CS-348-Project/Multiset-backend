/*
Name: get_purchases_by_group_id.sql
Description: Get all purchases for a group
Usage: {group_id = 1}
Return: {id, name, category, group_id, total_cost, purchaser}
*/

-- prodorder p.id
SELECT p.id, name, category, total_cost, purchaser_user_id, first_name as purchaser_first_name, last_name as purchaser_last_name
FROM purchase p
JOIN multiset_user u ON p.purchaser_user_id = u.id
WHERE purchaser_group_id = 1
ORDER BY p.id
LIMIT 10