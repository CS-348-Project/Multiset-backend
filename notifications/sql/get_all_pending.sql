/*
Name: get_all_pending.sql
Description: Gets all notifications that have not had an email sent for all 
             users with email notifications enabled.
*/

SELECT *, (
    -- get all notifications for the user
    SELECT json_agg(n)
    FROM (
        SELECT n.*
        FROM notification n
        WHERE n.user_id = u.id AND n.email_sent = FALSE
        ORDER BY n.created_at ASC -- oldest first
    ) n
) notifications
FROM multiset_user u
WHERE u.email_notifications = TRUE;