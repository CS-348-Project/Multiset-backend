SELECT first_name, last_name, email FROM multiset_user WHERE id = 3;
/*
begin expected
[
    {
        "first_name": "Carol",
        "last_name": "Hirose",
        "email": "carol@gmail.com"
    }
]
end expected
*/