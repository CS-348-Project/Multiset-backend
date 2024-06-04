/*
Name: get_settlements_by_member_id.sql
Description: Get all settlements for a member, both sending and receiving
Usage: {member_id}
*/
SELECT * FROM settlement_history
WHERE sender_id = %(member_id)s OR receiver_id = %(member_id)s;