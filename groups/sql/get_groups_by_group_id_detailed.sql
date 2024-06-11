/*
Name: get_groups_by_group_id_detailed.sql
Description: Get a group by its group_id
Usage: {group_id}
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
WHERE m.group_id = %(group_id)s
GROUP BY mg.id;
