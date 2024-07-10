/*
Name: get_email.sql
Description: Retrieves the user's email notification setting.
*/

SELECT email_notifications FROM multiset_user WHERE id = 200000;