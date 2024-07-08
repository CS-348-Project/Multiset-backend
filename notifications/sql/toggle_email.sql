/*
Name: toggle.sql
Description: Toggles the user's email notification setting.
*/

UPDATE multiset_user SET email_notifications = NOT email_notifications 
WHERE id = %(user_id)s RETURNING email_notifications;