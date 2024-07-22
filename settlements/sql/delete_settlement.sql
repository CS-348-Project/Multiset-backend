/*
Name: delete_settlement_by_id.sql
Description: Delete settlement based on settlement id
Usage: {settlement_id}
*/
DELETE FROM settlement_history
WHERE id = %(settlement_id)s;