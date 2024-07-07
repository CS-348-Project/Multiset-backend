/*
Name: get_triggers
Description: Get all triggers in the database
*/

SELECT trigger_name, event_object_table FROM information_schema.triggers;
