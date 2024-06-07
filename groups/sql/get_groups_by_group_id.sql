/*
Name: get_groups_by_group_id.sql
Description: Get a group by its group_id
Usage: {group_id}
*/

SELECT * FROM multiset_group
WHERE id = %(group_id)s;