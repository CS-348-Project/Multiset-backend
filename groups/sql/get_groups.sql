/*
Name: get_groups.sql
Description: Get all groups
Usage: {detailed}
*/

SELECT mg.*,
  CASE 
    WHEN %(detailed)s::boolean = TRUE THEN (
      SELECT json_agg(m.user_id) 
      FROM member m 
      WHERE m.group_id = mg.id) 
    ELSE NULL 
  END AS user_ids 
FROM multiset_group mg;