from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)

from dotenv import load_dotenv
import os


# load env variables
load_dotenv()


# Neon PostgreSQL URL
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing"
    )


# create connection
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


# DB session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# Base model
Base = declarative_base()


# dependency
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()