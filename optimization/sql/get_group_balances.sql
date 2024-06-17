/*
Name: get_group_balances.sql
Description: Get balances of all members in a group between each other. Accounts for purchases within the group and settlements
between two group members.
Usage: [group_id]
Return: [from_user_id, from_first_name, from_last_name, to_user_id, to_first_name, to_last_name, group_id, amount]
*/

WITH group_members AS (
    SELECT m.*, u.first_name, u.last_name 
    FROM member m, multiset_user u WHERE group_id = %(group_id)s AND m.user_id = u.id
),

-- get all users in a group
group_purchase_splits AS (
    SELECT borrower_user_id from_user_id, purchaser_user_id to_user_id, SUM(amount) purchase_amount
    FROM purchase_splits ps, purchase p
    WHERE ps.purchase_id IN (SELECT id FROM purchase WHERE purchaser_group_id = %(group_id)s)
    AND ps.purchase_id = p.id
    AND borrower_user_id != purchaser_user_id
    GROUP BY borrower_user_id, purchaser_user_id
),

group_settlements AS (
    SELECT sender_user_id from_user_id, receiver_user_id to_user_id, SUM(-amount) settlement_amount
    FROM settlement_history
    WHERE sender_group_id = %(group_id)s AND receiver_group_id = %(group_id)s
    AND sender_user_id != receiver_user_id
    GROUP BY sender_user_id, receiver_user_id
),

--this table may have balances both ways for a pair of users
uncondensed AS (
SELECT 
    from_user_id, to_user_id, %(group_id)s group_id, 
    COALESCE(purchase_amount, 0) + COALESCE(settlement_amount, 0) amount
    FROM group_purchase_splits NATURAL FULL OUTER JOIN group_settlements
),
 
condensed AS (
    --condense the balances for each pair of users
    SELECT u1.from_user_id, u1.to_user_id, u1.group_id, u1.amount - COALESCE(u2.amount,0) amount
    FROM uncondensed u1 LEFT OUTER JOIN uncondensed u2 
    ON u1.from_user_id = u2.to_user_id AND u1.to_user_id = u2.from_user_id
    WHERE u1.amount > u2.amount OR u2.amount IS NULL
)

SELECT c.*, 
gm1.first_name from_first_name, 
gm1.last_name from_last_name,
gm2.first_name to_first_name,
gm2.last_name to_last_name

FROM condensed c, group_members gm1, group_members gm2
WHERE c.from_user_id = gm1.user_id AND c.to_user_id = gm2.user_id;