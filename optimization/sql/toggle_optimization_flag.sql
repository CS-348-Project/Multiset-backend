/*
Name: toggle_optimization_flag.sql
Description: Toggles the optimization flag for a given group.
Usage: [group_id]
Return: [optimize_payments]
*/

UPDATE multiset_group 
SET optimize_payments = NOT optimize_payments WHERE id = %(group_id)s RETURNING optimize_payments;