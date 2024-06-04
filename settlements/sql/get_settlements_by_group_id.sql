/*
Name: get_settlements_by_group_id.sql
Description: Get all settlements for a group
Usage: {group_id}
*/
SELECT * FROM settlement_history
JOIN member ON settlement_history.receiver_id = member.id OR settlement_history.sender_id = member.id
WHERE member.group_id = %(group_id)s;