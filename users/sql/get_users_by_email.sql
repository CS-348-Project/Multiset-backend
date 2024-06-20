/*
Name: get_users_by_email.sql
Description: Get users by their email
Usage: { email }
*/

SELECT u.*
FROM multiset_user u
WHERE u.email = %(email)s;
