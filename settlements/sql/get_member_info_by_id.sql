/*
Name: get_member_info_by_id.sql
Description: Get member info (id, first_name, last_name) by id
Usage: {member_id}
*/
SELECT member.id as member_id, multiset_user.first_name, multiset_user.last_name FROM multiset_user 
JOIN member ON member.user_id = multiset_user.id 
WHERE member.id = %(member_id)s;