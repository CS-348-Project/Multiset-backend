/*
Name: verify_user_in_group
Description: Verify that a user is in a group
Usage: {user_id, group_id}
*/

SELECT COUNT(*) AS count FROM member 
WHERE user_id = %(user_id)s AND group_id = %(group_id)s;