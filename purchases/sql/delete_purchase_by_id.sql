/*
Name: delete_purchase_by_id.sql
Description: Delete purchase by purchase id
Usage: {purchase_id}
Return: {}
*/

DELETE FROM purchase WHERE id = %(purchase_id)s