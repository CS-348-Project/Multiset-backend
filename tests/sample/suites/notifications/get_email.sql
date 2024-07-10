/*
Name: get_email.sql
Description: Retrieves the user's email notification setting.
user_id = 2
*/

SELECT email_notifications FROM multiset_user WHERE id = 2;