from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, primary_key=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    salt = Column(String)