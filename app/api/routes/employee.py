from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

employees_db = {
    "emp001": "admin123"
}

class LoginRequest(BaseModel):
    id: str
    password: str

@router.post("/employee-login")
def employee_login(data: LoginRequest):
    if data.id in employees_db:
        if employees_db[data.id] == data.password:
            return {"status": "success", "role": "employee"}
        raise HTTPException(status_code=403, detail="Unauthorized employee")