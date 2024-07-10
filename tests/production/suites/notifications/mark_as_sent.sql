/*
Name: mark_as_sent.sql
Description: Marks a notification as email sent.
Usage: id=125000
*/

UPDATE notification SET email_sent = TRUE WHERE id = 125000;