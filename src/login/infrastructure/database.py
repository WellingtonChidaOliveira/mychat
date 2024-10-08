from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine("postgresql://myuser:mypassword@localhost:5432/chatbot_db")
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
    if inspector.has_table("users"):
        print("Table 'users' exists.")
    else:
        print("Warning: Table 'users' does not exist. Please ensure it's created manually.")
    
    print("Tables in the database:", inspector.get_table_names())

if __name__ == "__main__":
    init_db()