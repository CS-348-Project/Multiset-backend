/*
Name: get_groups_by_user_id.sql
Description: Get a group by its user_id
Usage: {user_id, detailed}
*/

SELECT mg.*
FROM multiset_group mg, member m
WHERE m.user_id = %(user_id)s AND mg.id = m.group_id;
