/*
Name: save_settlement.sql
Description: Save a settlement between two members
Usage: {sender_user_id, sender_group_id, receiver_user_id, receiver_group_id, amount}
*/
INSERT INTO settlement_history (sender_user_id, sender_group_id, receiver_user_id, receiver_group_id, amount) 
VALUES (%(sender_user_id)s, %(sender_group_id)s, %(receiver_user_id)s, %(receiver_group_id)s, %(amount)s)