from datetime import datetime
from ninja import Schema

class MemberActivityLog(Schema):
  id: int
  member_group_id: int
  member_user_id: int
  action: str
  details: str
  created_at: datetime