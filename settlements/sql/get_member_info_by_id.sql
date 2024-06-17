/*
Name: get_member_info_by_id.sql
Description: Get member info (user_id, group_id, first_name, last_name) by id
Usage: {member_user_id, member_group_id}
*/
SELECT %(member_user_id)s as member_user_id, %(member_group_id)s as member_group_id, multiset_user.first_name, multiset_user.last_name FROM multiset_user 
WHERE multiset_user.id = %(member_user_id)s;