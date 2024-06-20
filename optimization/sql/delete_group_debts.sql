/*
Name: delete_group_debts.sql
Description: Delete all current debts between group members for later recalculation
Usage: [group_id]
*/

DELETE FROM cumulative_debts 
WHERE borrower_group_id = %(group_id)s AND collector_group_id = %(group_id)s;