    
import bcrypt
from src.auth.infrastructure.database.repositories.user_repository import UserRepository
from ...domain.entities.user import User


class LoginUseCase:    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def execute(self, user_email: str, user_password: str) -> User:
        existing_user = self.user_repository.get_by_email(user_email)
        if not existing_user:
            raise ValueError("User not already exists.")
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), existing_user.salt.encode('utf-8'))
        if not bcrypt.checkpw(user_password.encode('utf-8'), hashed_password):
            raise ValueError("Invalid data.")
        
        return existing_user