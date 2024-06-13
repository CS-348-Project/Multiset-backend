/*
Name: add_users_to_group.sql
Description: Add users into a group
Usage: {user_ids, group_id}
*/

WITH user_ids AS (
  SELECT * FROM unnest(%(user_ids)s) AS id
)
INSERT INTO member ("user_id", "group_id")
SELECT u.id as user_id, %(group_id)s as group_id
FROM user_ids u;