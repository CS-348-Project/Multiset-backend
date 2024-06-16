/*
Name: get_aggregate_balances.sql
Description: Get balances of all members in a group (as an amount above or below zero). 
Accounts for purchases within the group and settlements between two group members.
Usage: [group_id]
Return: [user_id, group_id, first_name, last_name, balance]
*/

-- get all users in a group
WITH group_members AS (
    SELECT m.*, u.first_name, u.last_name 
    FROM member m, multiset_user u WHERE group_id = %(group_id)s AND m.user_id = u.id
),

purchase_owed AS (
    SELECT purchaser_user_id user_id, SUM(total_cost) amount
    FROM purchase p, group_members gm
    WHERE purchaser_group_id = %(group_id)s AND purchaser_group_id = group_id AND purchaser_user_id = user_id
    GROUP BY purchaser_user_id
),

purchase_owing AS (
    SELECT borrower_user_id user_id, SUM(amount) amount
    FROM purchase_splits ps
    WHERE ps.purchase_id IN (SELECT id FROM purchase WHERE purchaser_group_id = %(group_id)s)
    GROUP BY borrower_user_id
),

-- get the balances
in_group_settlements AS (
    SELECT *
    FROM settlement_history
    WHERE sender_group_id = %(group_id)s AND receiver_group_id = %(group_id)s
    AND sender_user_id IN (SELECT user_id FROM group_members) 
    AND receiver_user_id IN (SELECT user_id FROM group_members)
),

settlements_sent AS (
    SELECT sender_user_id user_id, SUM(amount) amount
    FROM in_group_settlements
    GROUP BY sender_user_id
),

settlements_received AS (
    SELECT receiver_user_id user_id, SUM(amount) amount
    FROM in_group_settlements
    GROUP BY receiver_user_id
)
-- big ugly query to get the balances for each person
-- purchase balance: amount owed - amount owing
-- settlement balance: amount sent - amount received
-- total balance: purchase balance + settlement balance
-- positive = owed money, negative = owing money

SELECT powing.user_id, 
        powing.group_id group_id,
        powing.first_name, 
        powing.last_name,
        -- COALESCE handles null values
        COALESCE(powed.amount, 0) - COALESCE(powing.amount, 0) + COALESCE(ssent.amount, 0) - COALESCE(sreceived.amount, 0) balance
FROM 
    -- right outer join to include all members in the group in each table
    -- natural join results in joining on user_id
    (purchase_owing NATURAL RIGHT OUTER JOIN group_members) powing, 
    (purchase_owed NATURAL RIGHT OUTER JOIN group_members) powed,
    (settlements_sent NATURAL RIGHT OUTER JOIN group_members) ssent,
    (settlements_received NATURAL RIGHT OUTER JOIN group_members) sreceived
WHERE powing.user_id = powed.user_id AND powing.user_id = ssent.user_id AND powing.user_id = sreceived.user_id; 
-- we use user_id (from group_members table at the top) because other columns might be null 