/*
Name: get_purchase_category_count.sql
Description: Get the count of purchases in each category for a group
Usage: [group_id]
Return: {category, count}
*/

SELECT category, COUNT(*)
FROM purchase
WHERE purchaser_group_id = %(group_id)s
GROUP BY category