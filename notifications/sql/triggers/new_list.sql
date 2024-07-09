/*
Name: new_list.sql
Description: Creates trigger to notify the user when a new grocery list is created in a group they are a member of.
*/

CREATE OR REPLACE FUNCTION notify_new_grocery_list() RETURNS trigger AS $new_list$
BEGIN
    INSERT INTO notification (user_id, message)
    (
        SELECT user_id, 
        'The grocery list ' || NEW.name || ' has been created in ' || g.name AS message
        FROM multiset_group g, member m
        WHERE g.id = m.group_id AND NEW.group_id = g.id
    );
    RETURN NEW;
END;
$new_list$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER notify_new_list_trigger
AFTER INSERT ON grocery_list
FOR EACH ROW
EXECUTE FUNCTION notify_new_grocery_list();