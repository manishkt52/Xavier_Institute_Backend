from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from app.api.routes import student, employee
from app.api.routes import auth
from app.db.database import Base, engine
from app.models import user
from app.api.routes import payment


Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://xavier-institute-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(employee.router)
app.include_router(payment.router)