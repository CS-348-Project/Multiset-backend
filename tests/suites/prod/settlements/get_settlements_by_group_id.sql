/*
Name: get_settlements_by_group_id.sql
Description: Get all settlements for a group
Usage: {group_id = 1}
*/
-- prodorder settlements.id;
WITH settlements AS (
  SELECT * FROM settlement_history
  WHERE sender_group_id = 1 AND receiver_group_id = 1
)

SELECT settlements.*, m1.first_name AS sender_first_name, m1.last_name AS sender_last_name, m2.first_name AS receiver_first_name, m2.last_name AS receiver_last_name
FROM settlements
JOIN multiset_user m1 ON settlements.sender_user_id = m1.id
JOIN multiset_user m2 ON settlements.receiver_user_id = m2.id
ORDER BY settlements.id LIMIT 10;
