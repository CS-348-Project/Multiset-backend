/*
Name: grocery_list_triggers.sql
Description: triggers for logging member activity on grocery list items
*/
CREATE OR REPLACE FUNCTION log_member_activity_grocery_list_item()
RETURNS TRIGGER AS $$
DECLARE
  detail_message TEXT;
  member_user_id INT;
  member_group_id INT;
  member_exists BOOLEAN;
BEGIN
  IF TG_OP = 'INSERT' THEN
    detail_message := 'Grocery list item "' || NEW.item_name || '" has been added by ' || 
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.requester_user_id);
    member_user_id := NEW.requester_user_id;
    member_group_id := NEW.requester_group_id;
  ELSIF TG_OP = 'UPDATE' THEN
    detail_message := 'Grocery list item "' || NEW.item_name || '" has been updated';
    member_user_id := NEW.requester_user_id;
    member_group_id := NEW.requester_group_id;
  ELSE
    detail_message := 'Grocery list item "' || OLD.item_name || '" has been deleted';
    member_user_id := OLD.requester_user_id;
    member_group_id := OLD.requester_group_id;
  END IF;

  -- Check if the member still exists
  SELECT EXISTS (SELECT 1 FROM member WHERE user_id = member_user_id AND group_id = member_group_id) INTO member_exists;

  IF member_exists THEN
    INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
    VALUES (member_user_id, member_group_id, TG_OP, detail_message);
  END IF;

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

CREATE OR REPLACE TRIGGER grocery_list_item_after_delete
AFTER DELETE ON grocery_list_item
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_grocery_list_item();