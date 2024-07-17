/*
Name: get_settlements_by_member_id.sql
Description: Get all settlements for a member, both sending and receiving
Usage: {member_user_id = 1, member_group_id = 1}
*/
WITH settlements AS (
  SELECT * FROM settlement_history
  WHERE sender_group_id = 1 AND receiver_group_id = 1
  AND (sender_user_id = 1 OR receiver_user_id = 1)
)

SELECT settlements.*, m1.first_name AS sender_first_name, m1.last_name AS sender_last_name, m2.first_name AS receiver_first_name, m2.last_name AS receiver_last_name
FROM settlements
JOIN multiset_user m1 ON settlements.sender_user_id = m1.id
JOIN multiset_user m2 ON settlements.receiver_user_id = m2.id;