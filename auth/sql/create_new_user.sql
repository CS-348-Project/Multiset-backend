INSERT INTO multiset_user 
(email, first_name, last_name, google_id)
VALUES (%(email)s, %(first_name)s, %(last_name)s, %(google_id)s)
RETURNING id