from multiset.db_utils import execute_query
from pathlib import Path

from .models import SettlementCreate

def add_member_info_to_settlements(settlements):
    # Parse the rows to add in member data 
    for settlement in settlements:
        settlement['sender'] = {
            'user_id': settlement['sender_user_id'],
            'group_id': settlement['sender_group_id'],
            'first_name': settlement['sender_first_name'],
            'last_name': settlement['sender_last_name'],
        }
        settlement['receiver'] = {
            'user_id': settlement['receiver_user_id'],
            'group_id': settlement['receiver_group_id'],
            'first_name': settlement['receiver_first_name'],
            'last_name': settlement['receiver_last_name'],
        }
        for key in ['sender_user_id', 'sender_group_id', 'sender_first_name', 'sender_last_name', 'receiver_user_id', 'receiver_group_id', 'receiver_first_name', 'receiver_last_name']:
            del settlement[key]
    return settlements

def find_settlements(group_id, member_user_id=None):
    if member_user_id:
        settlements = execute_query(
            Path("settlements/sql/get_settlements_by_member_id.sql"),
            {'member_user_id': member_user_id, 'member_group_id': group_id},
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

def find_settlements_between_members(member1_user_id, member2_user_id, group_id):
    settlements = execute_query(
        Path("settlements/sql/get_settlements_between_members.sql"),
        {'member1_user_id': member1_user_id, 'member2_user_id': member2_user_id, 'group_id': group_id},
        fetchall=True,
    )
    settlements = add_member_info_to_settlements(settlements)
    return settlements if settlements else []

def save_settlement(new_settlement: SettlementCreate):
    execute_query( 
        Path("settlements/sql/save_settlement.sql"), 
        {'sender_user_id': new_settlement.sender_user_id, 
         'receiver_user_id': new_settlement.receiver_user_id, 
         'sender_group_id': new_settlement.group_id,
         'receiver_group_id': new_settlement.group_id, 
         'amount': new_settlement.amount},
    )
    return True
