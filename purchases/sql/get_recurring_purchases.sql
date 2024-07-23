/*
Name: get_recurring_purchases.sql
Description: Get a user's purchased items where count >= 2
Usage: [group_id]
Return: {name, category, total cost}
*/

SELECT p.name, p.category, p.total_cost
FROM purchase p
GROUP BY p.name, p.category, p.total_cost, p.purchaser_group_id
HAVING COUNT(*) >= 2 and p.purchaser_group_id = %(group_id)s;
