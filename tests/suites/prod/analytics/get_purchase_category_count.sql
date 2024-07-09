/*
Name: get_purchase_category_count.sql
Description: Get the count of purchases in each category for a group
Usage: {group_id = 1}
Return: {category, count}
*/
--prodorder id
SELECT category, COUNT(*)
FROM purchase
WHERE purchaser_group_id = 1
GROUP BY categor ORDER BY id LIMIT 10;