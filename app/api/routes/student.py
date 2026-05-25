from fastapi import APIRouter, HTTPException, Response
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

# 🔐 Your Google Client ID
GOOGLE_CLIENT_ID = "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"

# ✅ Allowed users (authorization)
ALLOWED_USERS = [
    "student1@gmail.com",
    "student2@gmail.com"
]

# manual login users
STUDENTS = {
    "stu101": "pass123",
    "stu102": "pass456",
}

class TokenRequest(BaseModel):
    token: str

class LoginRequest(BaseModel):
    user_id: str
    password: str

@router.post("/student-login")
def student_login(data: TokenRequest):
    try:
        # ✅ Verify Google token
        idinfo = id_token.verify_oauth2_token(
            data.token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")

        # 🔐 Authorization check
        if email not in ALLOWED_USERS:
            raise HTTPException(status_code=403, detail="Unauthorized user")

        return {
            "status": "success",
            "role": "student",
            "email": email
        }

    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    

# Student Manual Login-in
# @router.post("/student-login-id")
# def student_login_id(
#     data: LoginRequest,
#     response: Response
# ):

#     if data.user_id not in STUDENTS:
#         raise HTTPException(
#             status_code=401,
#             detail="Invalid student ID"
#         )

#     if STUDENTS[data.user_id] != data.password:
#         raise HTTPException(
#             status_code=401,
#             detail="Wrong password"
#         )

#     response.set_cookie(
#         key="student_auth",
#         value=data.user_id,
#         httponly=True,
#         samesite="lax"
#     )

#     return {
#         "status": "success",
#         "role": "student",
#         "user_id": data.user_id
#     }    