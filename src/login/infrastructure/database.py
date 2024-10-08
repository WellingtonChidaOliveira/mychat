from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
assert DATABASE_URL is not None, "DATABASE_URL environment variable is not set"

engine = create_engine(DATABASE_URL)
Session_db = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

def get_session():
    session = Session_db()
    try:
        yield session
    finally:
        session.close()

