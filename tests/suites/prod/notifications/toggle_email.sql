/*
Name: toggle.sql
Description: Toggles the user's email notification setting.
user_id = 25000
*/

UPDATE multiset_user SET email_notifications = NOT email_notifications 
WHERE id = 25000 RETURNING email_notifications;