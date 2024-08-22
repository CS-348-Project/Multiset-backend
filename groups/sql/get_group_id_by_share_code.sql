/*
Name: get_group_id_by_share_code
Description: Gets a group id by a share code
Usage: {share_code}
*/

SELECT id
FROM multiset_group
WHERE share_code = %(share_code)s