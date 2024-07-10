/*
Name: new_purchase.sql
Description: Creates trigger to notify the user when they owe money for a purchase.
*/

CREATE OR REPLACE FUNCTION notify_new_purchase() RETURNS trigger AS $new_purchase$
BEGIN
    -- no nested subqueries in WHEN so we handle the case for the purchaser's split here
    IF (SELECT purchaser_user_id FROM purchase WHERE id = NEW.purchase_id) != NEW.borrower_user_id THEN
        INSERT INTO notification (user_id, message)
        (
            SELECT NEW.borrower_user_id user_id, 
            'You owe $' || ROUND(CAST(NEW.amount AS NUMERIC) / 100.0, 2) || ' to ' || u.first_name || ' ' || u.last_name || ' for ' || p.name AS message
            FROM purchase p, multiset_user u
            WHERE p.id = NEW.purchase_id AND p.purchaser_user_id = u.id
        );
    END IF;

    RETURN NEW;
END;
$new_purchase$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER notify_new_purchase_trigger
AFTER INSERT ON purchase_splits
FOR EACH ROW
EXECUTE FUNCTION notify_new_purchase();