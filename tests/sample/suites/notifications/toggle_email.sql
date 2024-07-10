/*
Name: toggle.sql
Description: Toggles the user's email notification setting.
user_id = 5
*/

UPDATE multiset_user SET email_notifications = NOT email_notifications 
WHERE id = 5 RETURNING email_notifications;