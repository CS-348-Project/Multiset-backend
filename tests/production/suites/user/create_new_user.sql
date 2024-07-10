/*
Name: create_new_user.sql
Description: Creates a new user
Usage: {email = test@gmail.com, first_name = Bob, last_name = Smith, google_id = 123456}
Return: id
*/
INSERT INTO multiset_user 
(email, first_name, last_name, google_id)
VALUES ('test@gmail.com', 'Bob', 'Smith', '123456')
RETURNING id