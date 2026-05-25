from fastapi import APIRouter
from app.services.payment_service import create_payment_order

router = APIRouter()

@router.post("/create-order")
def create_order():
    order = create_payment_order(500)

    return {
        "status": "success",
        "order": order
    }