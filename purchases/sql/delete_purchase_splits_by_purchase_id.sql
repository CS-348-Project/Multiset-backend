/*
Name: delete_purchase_splits_by_purchase_id.sql
Description: delete the old purchase splits by the purchase id
Usage: {purchase_id}
Return: {}
*/

DELETE FROM purchase_splits
WHERE purchase_id = %(purchase_id)s