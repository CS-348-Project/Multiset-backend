/*
Name: get_settlement_by_id.sql
Description: Get settlement info based on settlement id
Usage: {settlement_id}
*/
SELECT * FROM settlement_history
WHERE id = %(settlement_id)s;