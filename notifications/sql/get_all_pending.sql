/*
Name: get_all_pending.sql
Description: Gets all notifications that have not had an email sent for all 
             users with email notifications enabled.
*/

SELECT n.* FROM notification n
JOIN multiset_user u ON n.user_id = u.id
WHERE u.email_notifications = TRUE AND n.email_sent = FALSE;