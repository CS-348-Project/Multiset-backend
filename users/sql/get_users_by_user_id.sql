/*
Name: get_users_by_user_id.sql
Description: Get users by their user id
Usage: { user_id }
*/

SELECT u.*
FROM multiset_user u
WHERE u.id = %(user_id)s;
