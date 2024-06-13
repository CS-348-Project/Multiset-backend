SELECT p.id, name, category, total_cost, purchaser, first_name as purchaser_first_name, last_name as purchaser_last_name
FROM purchase p
JOIN multiset_user u ON p.purchaser = u.id
WHERE purchaser = $(user_id)s