/*
Name: get_recurring_purchases.sql
Description: Get a user's purchased items where count > 2
Usage: [user_id]
Return: {name}
*/

SELECT p.name
FROM purchase p
GROUP BY p.name, p.purchaser_user_id
HAVING COUNT(*) > 2 and p.purchaser_user_id = %(user_id)s;