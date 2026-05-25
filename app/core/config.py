from dotenv import load_dotenv
import os

load_dotenv()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_SECRET = os.getenv("RAZORPAY_SECRET")

class Settings:
    CLIENT_ID: str = os.getenv("google_client_id")
    SECRET_KEY: str = os.getenv("supersecretkey")  # change this
    ALGORITHM: str = "HS256"

settings = Settings()    