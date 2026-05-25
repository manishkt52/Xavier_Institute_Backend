import razorpay
from app.core.config import (
    RAZORPAY_KEY_ID,
    RAZORPAY_SECRET
)

client = razorpay.Client(auth=(
    RAZORPAY_KEY_ID,
    RAZORPAY_SECRET
))


def create_payment_order(amount: int):
    order = client.order.create({
        "amount": amount * 100,  # ₹ → paise
        "currency": "INR",
        "payment_capture": 1
    })

    return order