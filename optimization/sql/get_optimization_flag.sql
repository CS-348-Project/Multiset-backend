/*
Name: get_optimization_flag.sql
Description: Gets the optimization flag for a given group.
Usage: [group_id]
Return: [optimize_payments]
*/


SELECT optimize_payments FROM multiset_group WHERE id = %(group_id)s;