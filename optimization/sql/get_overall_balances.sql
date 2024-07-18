/*
Name: get_overall_balances.sql
Description: Get all current debts between group members
Usage: [group_id]
*/

WITH group_debts AS (
    SELECT * FROM cumulative_debts
    WHERE borrower_group_id = %(group_id)s AND collector_group_id = %(group_id)s
),

group_users AS (
    SELECT * FROM multiset_user WHERE id IN (SELECT user_id FROM member WHERE group_id = %(group_id)s)
),

member_owing AS (
    SELECT borrower_user_id, SUM(amount) owing FROM group_debts GROUP BY borrower_user_id
),

member_owed AS (
    SELECT collector_user_id, SUM(amount) owed FROM group_debts GROUP BY collector_user_id
)

SELECT id, first_name, last_name, email, COALESCE(owed, 0) - COALESCE(owing, 0) AS balance
FROM (group_users LEFT OUTER JOIN member_owing ON group_users.id = member_owing.borrower_user_id)
LEFT OUTER JOIN member_owed ON group_users.id = member_owed.collector_user_id;