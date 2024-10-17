

import bcrypt
from src.auth.infrastructure.database.repositories.user_repository import UserRepository
from ...domain.entities.user import User


class RegisterUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def execute(self, username: str, email: str, password: str) -> User:
        existing_user = self.user_repository.get_by_email(email)
        if existing_user:
            raise ValueError("User already exists.")
        salt = bcrypt.gensalt().decode('utf-8')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
        new_user = User(username=username, email=email, hashed_password=hashed_password, salt=salt)
        self.user_repository.create(new_user)
        return new_user