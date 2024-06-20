from datetime import datetime
from ninja import Schema

# TODO: replace with member from group management
class SettlementMemberInfo(Schema):
    user_id: int
    group_id: int
    first_name: str
    last_name: str
    
class Settlement(Schema):
    id: int
    sender: SettlementMemberInfo
    amount: float
    receiver: SettlementMemberInfo
    created_at: datetime
    
class SettlementCreate(Schema):
    sender_user_id: int
    receiver_user_id: int
    group_id: int
    amount: float