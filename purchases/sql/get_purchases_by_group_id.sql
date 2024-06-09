/*
Name: get_purchases_by_group_id.sql
Description: Get all purchases for a group
Usage: [group_id]
Return: {id, name, category, group_id, total_cost, purchaser}
*/

SELECT * FROM purchase WHERE group_id = %(group_id)s