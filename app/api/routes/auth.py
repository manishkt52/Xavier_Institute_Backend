from fastapi import APIRouter, HTTPException, Depends, Response, Request
from pydantic import BaseModel
from app.services.auth_service import verify_google_token
from app.core.security import create_access_token, verify_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User


router = APIRouter()
security = HTTPBearer()


class TokenData(BaseModel):
    token: str
    
class LoginRequest(BaseModel):
    user_id: str
    password: str

@router.post("/auth/google")
def google_auth(data: TokenData, response: Response, db: Session = Depends(get_db)):
    user_data = verify_google_token(data.token)
    email = user_data["email"]
    name = user_data["name"]

    # Check if user exists
    user = db.query(User).filter(User.email == email).first()

    # If not → create user
    if not user:
        raise HTTPException(status_code=403, detail="User not authorized")

    # Create JWT
    payload = {
        "sub": user.email,
        "name": user.name,
        "role": user.role
    }

    access_token = create_access_token(payload)

    response.set_cookie(
    key="access_token",
    value=access_token,
    httponly=True,
    max_age=120,  # 2 minutes
    secure=False,  # True in production (HTTPS)
    samesite="lax"
    )

    return {
        "message": "User authenticated",
        "user": {
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
    }


# Manual Student Login
@router.post("/student-login-id")
def student_login_id(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    # check user by student ID
    user = (
        db.query(User)
        .filter(User.student_id == data.user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid student ID"
        )

    # check password
    if user.password != data.password:
        raise HTTPException(
            status_code=401,
            detail="Wrong password"
        )

    # create JWT
    payload = {
        "sub": user.email,
        "name": user.name,
        "role": user.role,
    }

    access_token = create_access_token(
        payload
    )

    # set cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=120,
        secure=False,
        samesite="lax",
    )

    return {
        "message":
            "Student authenticated",

        "user": {
            "email": user.email,
            "name": user.name,
            "role": user.role,
        },
    }


def verify_token(request: Request):
    token = request.cookies.get("access_token")
    # print("COOKIE TOKEN:", token) 

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = verify_access_token(token)
        # print("PAYLOAD:", payload)  # 👈 ADD THIS
        return payload
    except Exception as e:
        # print("JWT ERROR:", str(e))  # 👈 ADD THIS
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
def require_role(required_role: str):
    def role_checker(user=Depends(verify_token)):
        if user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker      


@router.get("/protected")
def protected_route(user=Depends(verify_token)):
    return {
        "message": "You are authorized",
        "user": user
    }

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="lax"
    )

    return {
        "message":
            "Logged out successfully"
    }

@router.get("/admin")
def admin_route(user=Depends(require_role("admin"))):
    return {
        "message": "Welcome Admin",
        "user": user
    }
