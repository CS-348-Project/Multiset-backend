/*
Name: member_trigers.sql
Description: triggers for logging member activity on groups
*/
CREATE OR REPLACE FUNCTION log_member_activity_members()
RETURNS TRIGGER AS $$
DECLARE
  detail_message TEXT;
  user_id INT;
  group_id INT;
BEGIN    
  IF TG_OP = 'INSERT' THEN
    detail_message := 'Member ' || 
      (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.user_id) 
      || ' has joined group ' || 
      (SELECT name FROM multiset_group WHERE multiset_group.id = NEW.group_id);
    user_id := NEW.user_id;
    group_id := NEW.group_id;
  END IF;

  INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
  VALUES (user_id, group_id, TG_OP, detail_message);
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER member_activity_after_insert_member
AFTER INSERT ON member
FOR EACH ROW
EXECUTE FUNCTION log_member_activity_members();