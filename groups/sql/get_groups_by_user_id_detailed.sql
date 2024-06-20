/*
Name: get_groups_by_user_id_detailed.sql
Description: Get a group with detailed user information querying by its user_id 
Usage: {user_id}
*/

SELECT mg.*, json_agg(json_build_object(
  'id', mu.id, 
  'email', mu.email, 
  'first_name', mu.first_name, 
  'last_name', mu.last_name)
) AS users
FROM multiset_group mg 
JOIN member m ON mg.id = m.group_id
JOIN multiset_user mu ON m.user_id = mu.id
WHERE mg.id IN (
  SELECT group_id
  FROM member
  WHERE user_id = %(user_id)s
)
GROUP BY mg.id;
