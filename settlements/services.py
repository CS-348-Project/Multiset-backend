from multiset.db_utils import load_sql, execute_query

def get_settlements():
    rows = execute_query(['settlements', 'sql', 'get_settlements.sql'], fetchall=True)
    if rows:
        return rows
    return None

def save_settlement(purchaser_id, amount, borrower_id):
    execute_query(['settlements', 'sql', 'add_settlement.sql'], [purchaser_id, amount, borrower_id])
    return True