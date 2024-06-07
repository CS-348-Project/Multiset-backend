/*
Name: get_groups_by_member_id.sql
Description: Get a group by its member_id
Usage: {member_id}
*/

SELECT group_id 
FROM member m
WHERE m.user_id = %(member_id)s;