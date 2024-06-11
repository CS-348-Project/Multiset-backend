/*
Name: get_groups.sql
Description: Get all groups
Usage: {}
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
GROUP BY mg.id;
