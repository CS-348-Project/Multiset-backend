/*
Name: get_member_activity_logs_by_group_id.sql
Description: retrieves all member activity logs for a group
Usage: {group_id}
*/
SELECT * FROM member_activity_logs WHERE member_group_id = %(group_id)s ORDER BY created_at DESC;