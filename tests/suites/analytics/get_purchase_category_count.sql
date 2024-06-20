/*
Name: get_purchase_category_count.sql
Description: Get the count of purchases in each category for a group
Usage: {group_id = 1}
Return: {category, count}
*/

SELECT category, COUNT(*)
FROM purchase
WHERE purchaser_group_id = 1
GROUP BY category