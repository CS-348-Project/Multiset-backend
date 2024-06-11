SELECT *
FROM purchase
WHERE group_id = %(group_id)s
AND purchaser = %(user_id)s