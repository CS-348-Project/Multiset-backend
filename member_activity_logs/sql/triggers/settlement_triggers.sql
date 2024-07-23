/*
Name: grocery_list_triggers.sql
Description: triggers for logging member activity on grocery list items
*/
CREATE OR REPLACE FUNCTION log_member_activity_settlements()
RETURNS TRIGGER AS $$
DECLARE
  detail_message TEXT;
  user_id INT;
  group_id INT;
BEGIN
  IF TG_OP = 'INSERT' THEN
    detail_message := 'Settlement of $' || ROUND(NEW.amount * 1. / 100, 2) || ' from ' ||
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.sender_user_id) ||
      ' to ' || (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.receiver_user_id) ||
      ' has been added';
    user_id := NEW.sender_user_id;
    group_id := NEW.sender_group_id;
  ELSIF TG_OP = 'UPDATE' THEN
    detail_message := 'Settlement of $' || ROUND(NEW.amount * 1. / 100, 2) || ' from ' ||
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.sender_user_id) ||
      ' to ' || (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.receiver_user_id) ||
      ' has been updated';
    user_id := NEW.sender_user_id;
    group_id := NEW.sender_group_id;
  ELSE
    detail_message := 'Settlement of $' || ROUND(OLD.amount * 1. / 100, 2) || ' from ' ||
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = OLD.sender_user_id) ||
      ' to ' || (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = OLD.receiver_user_id) ||
      ' has been deleted';
    user_id := OLD.sender_user_id;
    group_id := OLD.sender_group_id;
  END IF;

  INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
  VALUES (user_id, group_id, TG_OP, detail_message);
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER settlement_history_after_insert
AFTER INSERT ON settlement_history
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_settlements();

CREATE OR REPLACE TRIGGER settlement_history_after_update
AFTER UPDATE ON settlement_history
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_settlements();

CREATE OR REPLACE TRIGGER settlement_history_after_delete
AFTER DELETE ON settlement_history
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_settlements();