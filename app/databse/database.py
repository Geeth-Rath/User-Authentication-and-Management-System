from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

SQLITE_DATABASE_URL = os.getenv("DATABASE_URL")

database_name = os.getenv("DATABASE_NAME", "default_db_name")
database_url = f"sqlite:///./{database_name}.db"

engine = create_engine(
    database_url, echo=True, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

