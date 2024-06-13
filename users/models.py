from datetime import datetime
from ninja import Schema
from typing import List, Optional

class User(Schema):
    id: int
    user_token: str
    first_name: str
    last_name: str
    email: str
    password: str

