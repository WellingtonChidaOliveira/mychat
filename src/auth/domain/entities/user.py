from dataclasses import dataclass
from sqlalchemy import Column, String
from ....shared.infrastructure.database import Base

@dataclass  
class User(Base):
    __tablename__ = "users"
    username = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, primary_key=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    salt = Column(String)