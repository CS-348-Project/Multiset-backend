/*
Name: get_groups.sql
Description: Get all groups
Usage: {}
*/
--prodorder mg.id
SELECT mg.* FROM multiset_group mg ORDER BY mg.id LIMIT 10;