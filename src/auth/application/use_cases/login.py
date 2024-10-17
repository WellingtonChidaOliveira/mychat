    
import bcrypt
from src.auth.infrastructure.database.repositories.user_repository import UserRepository
from ...domain.entities.user import User


class LoginUseCase:    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        
    def execute(self, user_email: str, user_password: str) -> User:
        existing_user = self.user_repository.get_by_email(user_email)
        if not existing_user:
            raise ValueError("Invalid email or password")
        
        if not bcrypt.checkpw(user_password.encode('utf-8'), existing_user.hashed_password.encode('utf-8')):
            raise ValueError("Invalid email or password")
        
        return existing_user