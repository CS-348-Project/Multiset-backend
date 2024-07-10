/*
Name: get_top_spenders.sql
Description: Gets the num_purchases and total spent by each member of a group
Usage: {group_id = 1}
Return: {id, first_name, last_name, num_purchases, total_spend}
*/

-- prodorder u.id
SELECT u.id, u.first_name, u.last_name, COUNT(*) AS num_purchases, SUM(total_cost) AS total_spend
FROM multiset_user u
JOIN purchase p ON u.id = p.purchaser_user_id
WHERE p.purchaser_group_id = 1
GROUP BY u.id
ORDER BY SUM(total_cost) DES ORDER BY u.id;