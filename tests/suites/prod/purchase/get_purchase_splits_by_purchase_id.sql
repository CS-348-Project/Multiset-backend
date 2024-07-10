/*
Name: get_purchase_splits_by_purchase_id.sql
Description: Get purchase split details from purchase id
Usage: {purchase_id = 1}
Return: {purchase_id, amount, first_name, last_name}
*/
-- prodorder id
SELECT id, purchase_id, amount, first_name, last_name
FROM purchase_splits ps
JOIN multiset_user mu ON mu.id = ps.borrower_user_id 
WHERE purchase_id = 1
