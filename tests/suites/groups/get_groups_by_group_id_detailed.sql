/*
Name: get_groups_by_group_id_detailed.sql
Description: Get a group by its group_id with user details
Usage: {group_id = 1}
*/

SELECT mg.*, 
-- Aggregates all of the non-null users into a JSON array
-- In the case where there are no users, COALESCE converts the null value to an empty array
COALESCE(json_agg(json_build_object(
  'id', mu.id, 
  'email', mu.email, 
  'first_name', mu.first_name, 
  'last_name', mu.last_name)
) FILTER (WHERE mu.id IS NOT NULL), '[]') AS users  
FROM multiset_group mg 
LEFT JOIN member m ON mg.id = m.group_id
LEFT JOIN multiset_user mu ON m.user_id = mu.id
WHERE mg.id = 1
GROUP BY mg.id;
