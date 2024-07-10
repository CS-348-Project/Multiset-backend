/*
Name: save_settlement.sql
Description: Save a settlement between two members
Usage: {sender_user_id = 1, sender_group_id = 1, receiver_user_id = 2, receiver_group_id = 1, amount = 300}
*/
INSERT INTO settlement_history (sender_user_id, sender_group_id, receiver_user_id, receiver_group_id, amount) 
VALUES (1, 1, 2, 1, 300)