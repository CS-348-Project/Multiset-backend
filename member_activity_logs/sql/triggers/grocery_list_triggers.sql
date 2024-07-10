/*
Name: grocery_list_triggers.sql
Description: triggers for logging member activity on grocery list items
*/
CREATE OR REPLACE FUNCTION log_member_activity_grocery_list_item()
RETURNS TRIGGER AS $$
DECLARE
  detail_message TEXT;
  user_id INT;
  group_id INT;
BEGIN
  IF TG_OP = 'INSERT' THEN
    detail_message := 'Grocery list item "' || NEW.item_name || '" has been added by ' || 
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.requester_user_id);
    user_id := NEW.requester_user_id;
    group_id := NEW.requester_group_id;
  ELSE
    detail_message := 'Grocery list item "' || NEW.item_name || '" has been updated';
    user_id := NEW.requester_user_id;
    group_id := NEW.requester_group_id;
  END IF;

  INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
  VALUES (user_id, group_id, TG_OP, detail_message);
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER grocery_list_item_after_insert
AFTER INSERT ON grocery_list_item
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_grocery_list_item();

CREATE OR REPLACE TRIGGER grocery_list_item_after_update
AFTER UPDATE ON grocery_list_item
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_grocery_list_item();