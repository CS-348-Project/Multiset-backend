/*
Name: update_group.sql
Description: Update a group's properties based on its group_id
Usage: {group_id = 1, name = "Test Group", optimize_payments = true}
*/

UPDATE multiset_group
SET name = 'Test Group', optimize_payments = TRUE
WHERE id = 1;