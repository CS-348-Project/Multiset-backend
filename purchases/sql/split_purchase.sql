/*
Name: split_purchase.sql
Description: Insert a new row into the purchase_splits relation after a new purchase is made
Usage: [purchase_id, amount, borrower]
Return: None
*/
INSERT INTO purchase_splits (purchase_id, amount, borrower)
VALUES (%(purchase_id)s, %(amount)s, %(borrower)s) RETURNING id