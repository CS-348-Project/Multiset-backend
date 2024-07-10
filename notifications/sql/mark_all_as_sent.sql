/*
Name: mark_all_as_sent.sql
Description: Marks all notifications as email sent for the user.
Usage: [user_id]
*/

UPDATE notification SET email_sent = TRUE WHERE user_id = %(user_id)s;