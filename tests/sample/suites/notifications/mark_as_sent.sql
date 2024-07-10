/*
Name: mark_as_sent.sql
Description: Marks a notification as email sent.
Usage: id=12
*/

UPDATE notification SET email_sent = TRUE WHERE id = 12;