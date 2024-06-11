/*
Name: get_groups_by_group_id.sql
Description: Get a group by its group_id
Usage: {group_id, detailed}
*/

SELECT mg.*
FROM multiset_group mg
WHERE mg.id = %(group_id)s;