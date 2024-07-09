/*
Name: toggle_optimization_flag.sql
Description: Toggles the optimization flag for a given group.
Usage: {group_id: 1}
Return: [optimize_payments]
*/

UPDATE multiset_group 
SET optimize_payments = NOT optimize_payments WHERE id = 1 RETURNING optimize_payments;