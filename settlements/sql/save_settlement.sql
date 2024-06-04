/*
Name: save_settlement.sql
Description: Save a settlement between two members
Usage: {sender_id, receiver_id, amount}
*/
INSERT INTO settlement_history (sender_id, amount, receiver_id) 
VALUES (%(sender_id)s, %(amount)s, %(receiver_id)s);