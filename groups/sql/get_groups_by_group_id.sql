/*
Name: get_groups_by_group_id.sql
Description: Get a group by its group_id
Usage: {group_id, detailed}
*/

SELECT mg.*, 
  CASE 
    WHEN %(detailed)s::boolean = TRUE THEN (
      SELECT json_agg(m.user_id) 
      FROM member m 
      WHERE m.group_id = mg.id) 
    ELSE NULL 
  END AS user_ids
FROM multiset_group mg
WHERE mg.id = %(group_id)s;