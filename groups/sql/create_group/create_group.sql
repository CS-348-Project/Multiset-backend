/*
Name: create_group.sql
Description: Create a group
Usage: {name, optimize_payments}
*/


-- Create a new group and retrieve the group_id
INSERT INTO multiset_group ("name", "optimize_payments", "share_code")
VALUES (%(name)s, %(optimize_payments)s, %(share_code)s)
RETURNING *
