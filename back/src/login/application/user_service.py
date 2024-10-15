from datetime import datetime, timedelta, timezone
import os
import bcrypt
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from ..infrastructure.JWT.token import create_token
from ..domain.user import User
from ..infrastructure.user_repository import UserRepository
from ..schemas.user_schemas import UserLogin, UserCreate

load_dotenv()

ACCESS_TOKEN_EXPIRE_HOURS = os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")

def generate_token(data: dict):
        access_token_expires = timedelta(hours=int(ACCESS_TOKEN_EXPIRE_HOURS))
        return create_token(data, access_token_expires)
    
class UserService:
    def __init__(self, session: Session):
        self.user_repository = UserRepository(session)
        
        
   

    def login(self, user: UserLogin):
        existing_user = self.user_repository.get_by_email(user.email)
        if not existing_user:
            raise ValueError("User not already exists.")
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), existing_user.salt.encode('utf-8'))
        if not bcrypt.checkpw(user.password.encode('utf-8'), hashed_password):
            raise ValueError("Invalid data.")
        
        return generate_token(data={"sub": existing_user.email})
        

    def register(self, user: UserCreate):
        existing_user = self.user_repository.get_by_email(user.email)
        if existing_user:
            raise ValueError("User already exists.")
        salt = bcrypt.gensalt().decode('utf-8')
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password, salt=salt)
        self.user_repository.add(new_user)
        return generate_token(data={"sub": new_user.email})
        
    def delete(self, email: str):
        existing_user = self.user_repository.get_by_email(email)
        self.user_repository.delete(existing_user.id)
        
    