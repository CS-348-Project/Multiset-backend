/*
Name: create_group.sql
Description: Create a group and add its initial members
Usage: {name, optimize_payments, user_ids}
*/

BEGIN TRANSACTION; 
-- Create a new group and retrieve the group_id
WITH group_info AS (
  INSERT INTO multiset_group ("name", "optimize_payments")
  VALUES (%(name)s, %(optimize_payments)s)
  RETURNING id, "name", "optimize_payments"
),
user_ids AS (
  SELECT * FROM unnest(%(user_ids)s) AS id
)
-- Add the users to the group
INSERT INTO member ("user_id", "group_id")
SELECT u.id as user_id, g.id as group_id
FROM user_ids u, (SELECT * FROM group_info) g
RETURNING g.id as id, g.name as name, g.optimize_payments as optimize_payments;

COMMIT;