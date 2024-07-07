from django.db import migrations

class Migration(migrations.Migration):
  dependencies = [("multiset", "0001_db_setup"), ("multiset", "0002_add_indexes")]
  
  operations = [
    migrations.RunSQL(
      """
      CREATE OR REPLACE FUNCTION log_member_activity_members()
      RETURNS TRIGGER AS $$
      DECLARE
        detail_message TEXT;
        user_id INT;
        group_id INT;
      BEGIN    
        IF TG_OP = 'DELETE' THEN
          detail_message := 'Member ' || 
            (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = OLD.user_id)
            || ' has left group ' || 
            (SELECT name FROM multiset_group WHERE multiset_group.id = OLD.group_id);
          user_id := OLD.user_id;
          group_id := OLD.group_id;
        ELSIF TG_OP = 'INSERT' THEN
          detail_message := 'Member ' || 
            (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.user_id) 
            || ' has joined group ' || 
            (SELECT name FROM multiset_group WHERE multiset_group.id = NEW.group_id);
          user_id := NEW.user_id;
          group_id := NEW.group_id;
        END IF;

        INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
        VALUES (NEW.user_id, NEW.group_id, TG_OP, detail_message);
        RETURN NULL;
      END;
      $$ LANGUAGE plpgsql;
      
      CREATE OR REPLACE FUNCTION log_member_activity_purchases()
      RETURNS TRIGGER AS $$
      DECLARE
        detail_message TEXT;
        user_id INT;
        group_id INT;
      BEGIN
        IF TG_OP = 'DELETE' THEN
          detail_message := 'Purchase "' || OLD.name || '" has been deleted';
          user_id := OLD.purchaser_user_id;
          group_id := OLD.purchaser_group_id;
        ELSIF TG_OP = 'INSERT' THEN
          detail_message := 'Purchase "' || NEW.name || '" has been added by ' || 
            (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.purchaser_user_id);
          user_id := NEW.purchaser_user_id;
          group_id := NEW.purchaser_group_id;
        ELSE
          detail_message := 'Purchase "' || NEW.name || '" has been updated';
          user_id := NEW.purchaser_user_id;
          group_id := NEW.purchaser_group_id;
        END IF;

        INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
        VALUES (user_id, group_id, TG_OP, detail_message);
        RETURN NULL;
      END;
      $$ LANGUAGE plpgsql;
      
      CREATE OR REPLACE FUNCTION log_member_activity_settlements()
      RETURNS TRIGGER AS $$
      DECLARE
        detail_message TEXT;
        user_id INT;
        group_id INT;
      BEGIN
        IF TG_OP = 'DELETE' THEN
          detail_message := 'Settlement of ' || OLD.amount / 100 || ' from ' ||
            (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = OLD.sender_user_id) ||
            ' to ' || (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = OLD.receiver_user_id) ||
            ' has been deleted';
          user_id := OLD.sender_user_id;
          group_id := OLD.sender_group_id;
        ELSIF TG_OP = 'INSERT' THEN
          detail_message := 'Settlement of ' || NEW.amount / 100 || ' from ' ||
            (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.sender_user_id) ||
            ' to ' || (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.receiver_user_id) ||
            ' has been added';
          user_id := NEW.sender_user_id;
          group_id := NEW.sender_group_id;
        ELSE
          detail_message := 'Settlement of ' || NEW.amount / 100 || ' from ' ||
            (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.sender_user_id) ||
            ' to ' || (SELECT first_name || ' ' || last_name FROM multiset_user WHERE multiset_user.id = NEW.receiver_user_id) ||
            ' has been updated';
          user_id := NEW.sender_user_id;
          group_id := NEW.sender_group_id;
        END IF;

        INSERT INTO member_activity_logs (member_user_id, member_group_id, action, details)
        VALUES (user_id, group_id, TG_OP, detail_message);
        RETURN NULL;
      END;
      $$ LANGUAGE plpgsql;
      
      CREATE OR REPLACE FUNCTION log_member_activity_grocery_list_item()
      RETURNS TRIGGER AS $$
      DECLARE
        detail_message TEXT;
        user_id INT;
        group_id INT;
      BEGIN
        IF TG_OP = 'DELETE' THEN
          detail_message := 'Grocery list item "' || OLD.item_name || '" has been deleted';
          user_id := OLD.requester_user_id;
          group_id := OLD.requester_group_id;
        ELSIF TG_OP = 'INSERT' THEN
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
      
      CREATE TRIGGER member_activity_after_insert_member
      AFTER INSERT ON member
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_members();

      CREATE TRIGGER member_activity_after_delete_member
      AFTER DELETE ON member
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_members();

      CREATE TRIGGER purchase_after_insert
      AFTER INSERT ON purchase
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_purchases();

      CREATE TRIGGER purchase_after_update
      AFTER UPDATE ON purchase
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_purchases();

      CREATE TRIGGER purchase_after_delete
      AFTER DELETE ON purchase
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_purchases();

      CREATE TRIGGER settlement_history_after_insert
      AFTER INSERT ON settlement_history
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_settlements();

      CREATE TRIGGER settlement_history_after_update
      AFTER UPDATE ON settlement_history
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_settlements();

      CREATE TRIGGER settlement_history_after_delete
      AFTER DELETE ON settlement_history
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_settlements();

      CREATE TRIGGER grocery_list_item_after_insert
      AFTER INSERT ON grocery_list_item
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_grocery_list_item();

      CREATE TRIGGER grocery_list_item_after_update
      AFTER UPDATE ON grocery_list_item
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_grocery_list_item();

      CREATE TRIGGER grocery_list_item_after_delete
      AFTER DELETE ON grocery_list_item
      FOR EACH ROW
      EXECUTE FUNCTION log_member_activity_grocery_list_item();
      """
    )
  ]