/*
Name: get_groups_by_user_id.sql
Description: Get a group by its user_id
Usage: {user_id, detailed}
*/

SELECT mg.*, 
  CASE 
    WHEN %(detailed)s::boolean = TRUE THEN (
      SELECT json_agg(m.user_id) 
      FROM member m 
      WHERE m.group_id = mg.id) 
    ELSE NULL 
  END AS user_ids
FROM multiset_group mg, member m
WHERE m.user_id = %(user_id)s AND mg.id = m.group_id;
