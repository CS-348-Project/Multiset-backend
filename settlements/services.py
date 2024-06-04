from multiset.db_utils import execute_query
from pathlib import Path

from .models import Settlement


def find_settlements(group_id=None, member_id=None):
    if member_id:
        rows = execute_query(
            Path("settlements/sql/get_settlements_by_member_id.sql"),
            {'member_id': member_id},
            fetchall=True,
        )
    elif group_id:
        rows = execute_query(
            Path("settlements/sql/get_settlements_by_group_id.sql"),
            {'group_id': group_id},
            fetchall=True,
        )
    else:
        rows = execute_query(Path("settlements/sql/get_settlements.sql"), fetchall=True)
    return rows if rows else []

def find_settlements_between_members(member1_id, member2_id):
    rows = execute_query(
        Path("settlements/sql/get_settlements_between_members.sql"),
        {'member1_id': member1_id, 'member2_id': member2_id},
        fetchall=True,
    )
    return rows if rows else []

def save_settlement(new_settlement: Settlement):
    execute_query(
        Path("settlements/sql/save_settlement.sql"), 
        {'sender_id': new_settlement.sender_id, 'amount': new_settlement.amount, 'receiver_id': new_settlement.receiver_id},
    )
    return True
