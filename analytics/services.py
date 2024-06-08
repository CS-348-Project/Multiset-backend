from multiset.db_utils import execute_query
from purchases.models import Purchase
from purchases.services import get_purchases_by_group_id
from collections import defaultdict


def get_purchase_category_count(group_id: int):
    rows = get_purchases_by_group_id(group_id)
    categories = defaultdict(int)
    for row in rows:
        category = row["category"]
        if not category:
            continue
        categories[category] += 1

    return categories
