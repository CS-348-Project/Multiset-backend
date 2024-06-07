/*
Name: delete_group.sql
Description: Delete a group based on its group_id
Usage: {group_id}
*/

DELETE FROM multiset_group
WHERE id = %(group_id)s;