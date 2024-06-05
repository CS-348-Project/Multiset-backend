/*
Name: get_balances.sql
Description: Get balances of all members in a group. Accounts for purchases within the group and settlements
between two group members.
Usage: [groupId]
*/

-- get all users in a group
WITH user_ids AS (
    SELECT user_id id FROM member WHERE group_id = %(group_id)s
),

purchase_owed AS (
    SELECT purchaser, SUM(total_cost) amount
    FROM purchase p
    WHERE p.group_id = %(group_id)s
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
    WHERE sender_id IN (SELECT id FROM user_ids) AND receiver_id IN (SELECT id FROM user_ids)
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

SELECT powing.id user_id, 
    -- COALESCE handles null values
    COALESCE(powed.amount, 0) - COALESCE(powing.amount, 0) + COALESCE(ssent.amount, 0) - COALESCE(sreceived.amount, 0) balance
FROM 
    (purchase_owing RIGHT OUTER JOIN user_ids ON user_ids.id = purchase_owing.borrower) powing, 
    (purchase_owed RIGHT OUTER JOIN user_ids ON user_ids.id = purchase_owed.purchaser) powed,
    (settlements_sent RIGHT OUTER JOIN user_ids ON user_ids.id = settlements_sent.sender_id) ssent,
    (settlements_received RIGHT OUTER JOIN user_ids ON user_ids.id = settlements_received.receiver_id) sreceived
WHERE powing.id = powed.id AND powing.id = ssent.id AND powing.id = sreceived.id; 
-- we use id (from user_ids table at the top) because other columns might be null 