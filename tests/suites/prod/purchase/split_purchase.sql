/*
Name: split_purchase.sql
Description: Insert a new row into the purchase_splits relation after a new purchase is made
Usage: [purchase_id, amount, borrower]
Return: None
*/
INSERT INTO purchase_splits (purchase_id, amount, borrower_user_id, borrower_group_id)
VALUES (1, 400, 10, 2)