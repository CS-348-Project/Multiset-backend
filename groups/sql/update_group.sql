/*
Name: update_group.sql
Description: Update a group's properties based on its group_id
Usage: {group_id, name, optimize_payments, budget}
*/

UPDATE multiset_group
SET name = %(name)s, optimize_payments = %(optimize_payments)s
WHERE id = %(group_id)s;