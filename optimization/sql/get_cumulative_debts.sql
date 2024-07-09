/*
Name: get_cumulative_debts.sql
Description: Get the cumulative debts of a group
*/

SELECT borrower_user_id from_user_id, u1.first_name from_first_name, u1.last_name from_last_name,
       collector_user_id to_user_id, u2.first_name to_first_name, u2.last_name to_last_name,
       amount
FROM cumulative_debts, multiset_user u1, multiset_user u2
WHERE borrower_user_id = u1.user_id AND collector_user_id = u2.user_id AND group_id = %(group_id)s