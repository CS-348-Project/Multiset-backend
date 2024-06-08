/*
Name: get_groups_by_user_id.sql
Description: Get a group by its user_id
Usage: {user_id}
*/

SELECT mg.*
FROM multiset_group mg
JOIN member m ON mg.id = m.group_id
WHERE m.user_id = %(user_id)s;