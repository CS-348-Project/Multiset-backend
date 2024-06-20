/*
Name: insert_debt.sql
Description: Adds a new debt between two users in a group
Usage: [amount=5000, borrower_user_id=3, collector_user_id=6, borrower_group_id=1, collector_group_id=1]
*/
INSERT INTO cumulative_debts (amount, borrower_user_id, collector_user_id, borrower_group_id, collector_group_id)
VALUES (5000, 3, 6, 1, 1)
RETURNING *;