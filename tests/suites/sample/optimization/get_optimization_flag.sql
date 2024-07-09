/*
Name: get_optimization_flag.sql
Description: Gets the optimization flag for a given group.
Usage: {group_id: 1}
Return: [optimize_payments]
*/


SELECT optimize_payments FROM multiset_group WHERE id = 1;