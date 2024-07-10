from django.db import migrations


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunSQL(
            """
      CREATE TABLE multiset_user (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        google_id VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        email_notifications BOOLEAN NOT NULL DEFAULT FALSE
      );
      
      CREATE TABLE multiset_group (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        optimize_payments BOOLEAN NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
      );
      
      CREATE TABLE member (
        user_id int NOT NULL REFERENCES multiset_user(id) ON DELETE CASCADE,
        group_id int NOT NULL REFERENCES multiset_group(id) ON DELETE CASCADE,
        PRIMARY KEY (user_id, group_id)
      );
      
      CREATE TABLE purchase (
        id SERIAL PRIMARY KEY,
        category VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        total_cost INT NOT NULL,
        purchaser_user_id INT NOT NULL,
        purchaser_group_id INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (purchaser_user_id, purchaser_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE
      );
      
      CREATE TABLE purchase_splits (
        purchase_id INT NOT NULL REFERENCES purchase(id) ON DELETE CASCADE,
        borrower_user_id INT NOT NULL,
        borrower_group_id INT NOT NULL,
        amount INT NOT NULL,
        PRIMARY KEY (purchase_id, borrower_user_id, borrower_group_id),
        FOREIGN KEY (borrower_user_id, borrower_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE
      );
      
      CREATE TABLE cumulative_debts (
        amount INT NOT NULL,
        collector_user_id INT NOT NULL,
        collector_group_id INT NOT NULL,
        borrower_user_id INT NOT NULL,
        borrower_group_id INT NOT NULL,
        PRIMARY KEY (collector_user_id, collector_group_id, borrower_user_id, borrower_group_id),
        FOREIGN KEY (collector_user_id, collector_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE,
        FOREIGN KEY (borrower_user_id, borrower_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE
      );
      
      CREATE TABLE settlement_history (
        id SERIAL PRIMARY KEY,
        sender_user_id INT NOT NULL,
        sender_group_id INT NOT NULL,
        receiver_user_id INT NOT NULL,
        receiver_group_id INT NOT NULL,
        amount INT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_user_id, sender_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE,
        FOREIGN KEY (receiver_user_id, receiver_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE
      );
      
      CREATE TABLE grocery_list (
        group_id INT NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        id SERIAL PRIMARY KEY,
        FOREIGN KEY (group_id) REFERENCES multiset_group(id) ON DELETE CASCADE
      );
      
      CREATE TABLE grocery_list_item (
        id SERIAL,
        grocery_list_id INT NOT NULL REFERENCES grocery_list(id) ON DELETE CASCADE,
        requester_user_id INT NOT NULL,
        requester_group_id INT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT FALSE,
        notes VARCHAR(255),
        quantity INT NOT NULL,
        item_name VARCHAR(255) NOT NULL,
        FOREIGN KEY (requester_user_id, requester_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE,
        PRIMARY KEY (id, grocery_list_id)
      );
      
      CREATE TABLE member_activity_logs (
        id SERIAL PRIMARY KEY,
        member_user_id INT NOT NULL,
        member_group_id INT NOT NULL,
        action VARCHAR(255) NOT NULL,
        details VARCHAR(255),
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (member_user_id, member_group_id) REFERENCES member(user_id, group_id) ON DELETE CASCADE
      );
      """
        )
    ]
