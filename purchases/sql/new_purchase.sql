INSERT INTO purchase (name, category, group_id, total_cost, purchaser)
VALUES (%(name)s, %(category)s, %(group_id)s, %(total_cost)s, %(purchaser)s) RETURNING id