from ninja import Schema

class Settlement(Schema):
    sender_id: int
    amount: float
    receiver_id: int