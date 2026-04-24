# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Dummy database (replace later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_users = {
    "student123": "password123",
    "john": "abc123"
}

class LoginRequest(BaseModel):
    student_id: str
    password: str

@app.get("/")
def home():
    return {"message": "Backend is running"}

@app.post("/student-login")
def student_login(data: LoginRequest):
    if data.student_id in fake_users:
        if fake_users[data.student_id] == data.password:
            return {
                "status": "success",
                "message": "Login successful"
            }
        else:
            raise HTTPException(status_code=401, detail="Wrong password")
    else:
        raise HTTPException(status_code=404, detail="User not found")