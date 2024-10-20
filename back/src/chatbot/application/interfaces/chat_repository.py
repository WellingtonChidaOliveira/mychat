

from abc import ABC, abstractmethod
from src.chatbot.domain.entities.chat import Chat


class ChatRepository(ABC):
    @abstractmethod
    async def create_chat(self, chat: Chat) -> Chat:
        pass
    
    @abstractmethod
    async def get_chat_by_id(self, chat_id: str) -> Chat:
        pass
    
    @abstractmethod
    async def delete_chat(self, chat_id: str, user_email: str) -> Chat:
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> list[Chat]:
        pass
    
    @abstractmethod
    async def update_chat(self, chat_id: int, user_message: str, full_response: str) -> Chat:
        pass