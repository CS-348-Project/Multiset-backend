/*
Name: purchase_triggers.sql
Description: triggers for logging member activity on purchases
*/
CREATE OR REPLACE FUNCTION log_member_activity_purchases()
RETURNS TRIGGER AS $$
DECLARE
  detail_message TEXT;
  user_id INT;
  group_id INT;
BEGIN
  IF TG_OP = 'INSERT' THEN
    detail_message := 'Purchase "' || NEW.name || '" has been added by ' || 
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.purchaser_user_id);
    user_id := NEW.purchaser_user_id;
    group_id := NEW.purchaser_group_id;
  ELSIF TG_OP = 'UPDATE' THEN
    detail_message := 'Purchase "' || NEW.name || '" has been updated';
    user_id := NEW.purchaser_user_id;
    group_id := NEW.purchaser_group_id;
  ELSE
    detail_message := 'Purchase "' || OLD.name || '" has been deleted';
    user_id := OLD.purchaser_user_id;
    group_id := OLD.purchaser_group_id;
  END IF;

  INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
  VALUES (user_id, group_id, TG_OP, detail_message);
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER purchase_after_insert
AFTER INSERT ON purchase
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_purchases();

CREATE OR REPLACE TRIGGER purchase_after_update
AFTER UPDATE ON purchase
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_purchases();

CREATE OR REPLACE TRIGGER purchase_after_delete
AFTER DELETE ON purchase
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_purchases();