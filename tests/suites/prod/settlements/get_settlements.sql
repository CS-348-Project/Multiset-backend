/*
Name: get_settlements.sql
Description: Get all settlements 
Usage: {}
*/
-- prodorder settlement_history.id;
SELECT settlement_history.*, m1.first_name AS sender_first_name, m1.last_name AS sender_last_name, m2.first_name AS receiver_first_name, m2.last_name AS receiver_last_name
FROM settlement_history
JOIN multiset_user m1 ON settlement_history.sender_user_id = m1.id
JOIN multiset_user m2 ON settlement_history.receiver_user_id = m2.id;