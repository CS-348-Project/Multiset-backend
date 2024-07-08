/*
Name: clear.sql
Description: Deletes all notifications for the user.
Usage: [user_id]
*/

DELETE FROM notification WHERE user_id = %(user_id)s;