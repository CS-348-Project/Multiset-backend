/*
Name: email_exists.sql
Description: Checks if a user exists with a given email
Usage: {email = 'teresamiller@gmail.com'}
Return: null
*/
SELECT id
FROM multiset_user
WHERE email = 'teresamiller@gmail.com';