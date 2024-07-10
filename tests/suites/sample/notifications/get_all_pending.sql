/*
Name: get_all_pending.sql
Description: Gets all notifications that have not had an email sent for all 
             users with email notifications enabled.
Usage:
*/

SELECT *, (
    -- get all notifications for the user
    SELECT json_agg(n)
    FROM (
        SELECT n.*
        FROM notification n
        WHERE n.user_id = u.id AND n.email_sent = FALSE
        ORDER BY n.created_at ASC -- oldest first
        LIMIT 3 -- only get the first 5
    ) n
) notifications
FROM multiset_user u
WHERE u.email_notifications = TRUE
ORDER BY u.id
LIMIT 10;