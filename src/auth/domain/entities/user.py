from dataclasses import dataclass
from sqlalchemy import Column, String
from ....shared.infrastructure.database import Base

@dataclass
class User(Base):
    __tablename__ = "users"
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True,primary_key=True ,index=True)
    hashed_password = Column(String)
    salt = Column(String)
    