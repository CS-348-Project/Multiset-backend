/*
Name: read.sql
Description: Marks all notifications as read for the user.
Usage: user_id=5
*/

UPDATE notification SET read = TRUE WHERE user_id = 5;