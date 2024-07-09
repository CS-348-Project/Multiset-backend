/*
Name: get_purchases_by_user_id_and_group_id.sql
Description: Get all purchases for a group and user id
Usage: {group_id = 1, user_id = 2}
Return: {id, name, category, group_id, total_cost, purchaser}
*/


SELECT p.id, name, category, total_cost, purchaser_user_id, first_name as purchaser_first_name, last_name as purchaser_last_name
FROM purchase p
JOIN multiset_user u ON p.purchaser_user_id = u.id
WHERE purchaser_group_id = 1
AND purchaser_user_id = 2