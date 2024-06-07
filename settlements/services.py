from multiset.db_utils import execute_query
from pathlib import Path

from .models import Settlement

def add_member_info_to_settlements(settlements):
    # Parse the rows to add in member data 
    for settlement in settlements:
        settlement['sender'] = execute_query(
            Path("settlements/sql/get_member_info_by_id.sql"),
            {'member_id': settlement['sender_id']},
            fetchone=True,
        )
        settlement['receiver'] = execute_query(
            Path("settlements/sql/get_member_info_by_id.sql"),
            {'member_id': settlement['receiver_id']},
            fetchone=True,
        )
        del settlement['sender_id']
        del settlement['receiver_id']
    return settlements

def find_settlements(group_id=None, member_id=None):
    if member_id:
        settlements = execute_query(
            Path("settlements/sql/get_settlements_by_member_id.sql"),
            {'member_id': member_id},
            fetchall=True,
        )
    elif group_id:
        settlements = execute_query(
            Path("settlements/sql/get_settlements_by_group_id.sql"),
            {'group_id': group_id},
            fetchall=True,
        )
    else:
        # TODO: pagination?
        settlements = execute_query(Path("settlements/sql/get_settlements.sql"), fetchall=True)
    settlements = add_member_info_to_settlements(settlements)
    return settlements if settlements else []

def find_settlements_between_members(member1_id, member2_id):
    settlements = execute_query(
        Path("settlements/sql/get_settlements_between_members.sql"),
        {'member1_id': member1_id, 'member2_id': member2_id},
        fetchall=True,
    )
    settlements = add_member_info_to_settlements(settlements)
    return settlements if settlements else []

def save_settlement(new_settlement: Settlement):
    execute_query(
        Path("settlements/sql/save_settlement.sql"), 
        {'sender_id': new_settlement.sender_id, 'amount': new_settlement.amount, 'receiver_id': new_settlement.receiver_id},
    )
    return True
