CREATE OR REPLACE FUNCTION notify_new_group() RETURNS trigger AS $new_group$
BEGIN
    INSERT INTO notification (user_id, message)
    (
        SELECT NEW.user_id, 'You have been added to ' || g.name AS message
        FROM multiset_group g
        WHERE g.id = NEW.group_id
    );
    RETURN NEW;
END;
$new_group$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER new_group_trigger
AFTER INSERT ON member
FOR EACH ROW
EXECUTE FUNCTION notify_new_group();