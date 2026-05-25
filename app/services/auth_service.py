from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException
from app.core.config import settings


def verify_google_token(token: str):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.CLIENT_ID
        )

        return {
            "email": idinfo.get("email"),
            "name": idinfo.get("name"),
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Google token")