/*
Name: add_users_to_group.sql
Description: Add users into a group
Usage: {user_ids, group_id}
*/

WITH user_ids AS (
  SELECT * FROM unnest(%(user_ids)s) AS id
)
INSERT INTO member ("user_id", "group_id")
SELECT u.id as user_id, g.id as $(group_id)s
FROM user_ids u, group_info g;