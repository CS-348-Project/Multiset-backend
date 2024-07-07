/*
Name: new_settlement.sql
Description: Creates trigger to notify the user when they receive a new settlement.
*/

CREATE OR REPLACE FUNCTION notify_new_settlement() RETURNS trigger AS $new_settlement$
BEGIN
    INSERT INTO notification (user_id, message)
    (
        SELECT NEW.receiver_user_id user_id, 
        'You have received a settlement of $' || ROUND(CAST(NEW.amount AS NUMERIC) / 100.0, 2) || ' from ' ||  u.first_name || ' ' || u.last_name AS message 
        FROM multiset_user u
        WHERE u.id = NEW.sender_user_id
    );
    RETURN NEW;
END;
$new_settlement$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER notify_new_settlement_trigger
AFTER INSERT ON settlement_history
FOR EACH ROW
EXECUTE FUNCTION notify_new_settlement();