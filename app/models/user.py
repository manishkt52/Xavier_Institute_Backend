from sqlalchemy import Column, Integer, String
from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String, default="user")

       # ✅ add these
    student_id = Column(
        String,
        unique=True,
        index=True,
        nullable=True
    )

    password = Column(
        String,
        nullable=True
    )