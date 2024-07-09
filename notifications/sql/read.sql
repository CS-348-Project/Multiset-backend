/*
Name: read.sql
Description: Marks all notifications as read for the user.
Usage: [user_id]
*/

UPDATE notification SET read = TRUE WHERE user_id = %(user_id)s;