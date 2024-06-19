from ninja import Schema

class User(Schema):
    id: int
    email: str
    google_id: str
    first_name: str
    last_name: str

