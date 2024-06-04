from ninja import Router
from .services import get_settlements, save_settlement

router = Router()

@router.get("/example")
def example(request):
    return "example"

# e.g. http://localhost:8000/api/settlements/
@router.get("/")
def get_settlements(request):
    return get_settlements()

# e.g. http://localhost:8000/api/settlements/add?purchaser_id=2&amount=200&borrower_id=3
# Remember that you must use Postman to test POST routes!
@router.post("/save")
def save_settlement(request, purchaser_id: int, amount: float, borrower_id: int):
    return save_settlement(purchaser_id, amount, borrower_id)
