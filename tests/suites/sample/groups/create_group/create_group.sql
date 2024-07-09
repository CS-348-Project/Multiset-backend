/*
Name: create_group.sql
Description: Create a group
Usage: {name = "Test Group", optimize_payments = false}
*/


-- Create a new group and retrieve the group_id
INSERT INTO multiset_group ("name", "optimize_payments")
VALUES ('Test Group', FALSE)
RETURNING *
