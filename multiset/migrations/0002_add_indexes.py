from django.db import migrations

class Migration(migrations.Migration):
  dependencies = [("multiset", "0001_db_setup")]
  
  operations = [
    migrations.RunSQL(
      """
      CREATE INDEX multiset_user_email_idx ON multiset_user (email);
      CREATE INDEX member_group_id_idx ON member (group_id);
      CREATE INDEX member_user_id_idx ON member (user_id);
      
      CREATE INDEX settlement_history_sender_group_id_idx ON settlement_history (sender_group_id);
      CREATE INDEX settlement_history_receiver_group_id_idx ON settlement_history (receiver_group_id);
      CREATE INDEX settlement_history_sender_idx ON settlement_history (sender_user_id, sender_group_id);
      CREATE INDEX settlement_history_receiver_idx ON settlement_history (receiver_user_id, receiver_group_id);
      
      CREATE INDEX cumulative_debts_borrower_idx ON cumulative_debts (borrower_user_id, borrower_group_id);
      CREATE INDEX cumulative_debts_collector_idx ON cumulative_debts (collector_user_id, collector_group_id);
      
      CREATE INDEX purchase_purchaser_idx ON purchase (purchaser_user_id, purchaser_group_id);
      CREATE INDEX purchase_purchaser_group_id_idx ON purchase (purchaser_group_id);
      
      CREATE INDEX purchase_splits_borrower_idx ON purchase_splits (borrower_user_id, borrower_group_id);
      CREATE INDEX purchase_splits_purchase_idx ON purchase_splits (purchase_id);
      
      CREATE INDEX grocery_list_group_id_idx ON grocery_list (group_id);
      CREATE INDEX grocery_list_item_grocery_list_id_idx ON grocery_list_item (grocery_list_id);
      CREATE INDEX grocery_list_item_item_name_idx ON grocery_list_item (item_name);
      
      CREATE INDEX member_activity_logs_group_id_idx ON member_activity_logs (member_group_id);
      """
    )
  ]