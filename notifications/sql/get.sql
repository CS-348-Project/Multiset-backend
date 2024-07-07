/*
Name: get.sql
Description: Retrieves all notifications for the user.
Usage: [user_id]
*/

SELECT * FROM notification WHERE user_id = %(user_id)s;