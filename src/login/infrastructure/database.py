from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://myuser:mypassword@localhost:5432/chatbot_db"

engine = create_engine(DATABASE_URL)
Session_db = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()

def get_session():
    session = Session_db()
    try:
        yield session
    finally:
        session.close()

def init_db():
    from src.login.domain.user import User  
    
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        print("Table 'users' does not exist. Creating it now.")
        Base.metadata.create_all(bind=engine)
    else:
        print("Table 'users' already exists.")
    
    print("Tables in the database:", inspector.get_table_names())

if __name__ == "__main__":
    init_db()