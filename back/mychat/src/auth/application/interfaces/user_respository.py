
from abc import ABC, abstractmethod
from ...domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> User:
        pass

    @abstractmethod
    def create(self, user: User):
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass
    
    