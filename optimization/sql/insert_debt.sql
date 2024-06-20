/*
Name: insert_debt.sql
Description: Adds a new debt between two users in a group
Usage: [amount, borrower_user_id, collector_user_id, borrower_group_id, collector_group_id]
*/
INSERT INTO cumulative_debts (amount, borrower_user_id, collector_user_id, borrower_group_id, collector_group_id)
VALUES (%(amount)s, %(borrower_user_id)s, %(collector_user_id)s, %(borrower_group_id)s, %(collector_group_id)s);