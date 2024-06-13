/*
Name: create_group.sql
Description: Create a group
Usage: {name, optimize_payments, budget}
*/


-- Create a new group and retrieve the group_id
INSERT INTO multiset_group ("name", "optimize_payments", "budget")
VALUES (%(name)s, %(optimize_payments)s, %(budget)s)
RETURNING *
