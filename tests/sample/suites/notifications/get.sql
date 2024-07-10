/*
Name: get.sql
Description: Retrieves all notifications for the user.
Usage: user_id=15
*/

SELECT * FROM notification WHERE user_id = 15 ORDER BY created_at DESC;