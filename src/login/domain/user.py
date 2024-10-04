from sqlalchemy import Column, String
from ..infrastructure.database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    salt = Column(String)