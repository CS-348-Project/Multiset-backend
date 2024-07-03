/*
Name: add_users_to_group.sql
Description: Add users into a group
Usage: {user_ids = [7, 8], group_id = 1}
*/

WITH user_ids AS (
  SELECT * FROM unnest(ARRAY[7, 8]) AS id
)
INSERT INTO member ("user_id", "group_id")
SELECT u.id as user_id, 1 as group_id
FROM user_ids u;