/*
Name: mark_as_sent.sql
Description: Marks a notification as email sent.
Usage: [notification_id]
*/

UPDATE notification SET email_sent = TRUE WHERE id = %(notification_id)s;