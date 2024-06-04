/*
Name: get_settlements_between_members.sql
Description: Get all settlements between two members
Usage: {member1_id, member2_id}
*/
SELECT * FROM settlement_history
WHERE sender_id = %(member1_id)s AND receiver_id = %(member2_id)s
OR sender_id = %(member2_id)s AND receiver_id = %(member1_id)s;