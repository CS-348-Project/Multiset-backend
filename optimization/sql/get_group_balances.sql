/*
Name: get_group_balances.sql
Description: Get balances of all members in a group. Accounts for purchases within the group and settlements
between two group members.
Usage: [group_id]
Return: [member_id, balance]
*/

-- get all users in a group
WITH group_members AS (
    SELECT m.*, u.first_name, u.last_name 
    FROM member m, multiset_user u WHERE group_id = %(group_id)s AND m.user_id = u.id
),

purchase_owed AS (
    SELECT purchaser, SUM(total_cost) amount
    FROM purchase p, group_members gm
    WHERE p.group_id = %(group_id)s AND p.purchaser = gm.id
    GROUP BY purchaser
),

purchase_owing AS (
    SELECT borrower, SUM(amount) amount
    FROM purchase_splits ps
    WHERE ps.purchase_id IN (SELECT id FROM purchase WHERE group_id = %(group_id)s)
    GROUP BY borrower
),

-- get the balances
in_group_settlements AS (
    SELECT *
    FROM settlement_history
    WHERE sender_id IN (SELECT id FROM group_members) AND receiver_id IN (SELECT id FROM group_members)
),

settlements_sent AS (
    SELECT sender_id, SUM(amount) amount
    FROM in_group_settlements
    GROUP BY sender_id
),

settlements_received AS (
    SELECT receiver_id, SUM(amount) amount
    FROM in_group_settlements
    GROUP BY receiver_id
)
-- big ugly query to get the balances for each person
-- purchase balance: amount owed - amount owing
-- settlement balance: amount sent - amount received
-- total balance: purchase balance + settlement balance
-- positive = owed money, negative = owing money

SELECT powing.id member_id, 
        powing.first_name, 
        powing.last_name,
        -- COALESCE handles null values
        COALESCE(powed.amount, 0) - COALESCE(powing.amount, 0) + COALESCE(ssent.amount, 0) - COALESCE(sreceived.amount, 0) balance
FROM 
    (purchase_owing RIGHT OUTER JOIN group_members ON group_members.id = purchase_owing.borrower) powing, 
    (purchase_owed RIGHT OUTER JOIN group_members ON group_members.id = purchase_owed.purchaser) powed,
    (settlements_sent RIGHT OUTER JOIN group_members ON group_members.id = settlements_sent.sender_id) ssent,
    (settlements_received RIGHT OUTER JOIN group_members ON group_members.id = settlements_received.receiver_id) sreceived
WHERE powing.id = powed.id AND powing.id = ssent.id AND powing.id = sreceived.id; 
-- we use id (from group_members table at the top) because other columns might be null 