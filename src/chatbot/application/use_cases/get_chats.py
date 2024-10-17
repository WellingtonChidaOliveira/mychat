from pytest import Session
from ..interfaces.chat_repository import ChatRepository

class GetChatsUseCase:
    def __init__(self, chat_repository: ChatRepository):
                self.chat_repository = chat_repository
                
                
    async def execute (self, user_email: str) :
            existing_chat_by_user = await self.chat_repository.get_chat_by_id(user_email)
            if not existing_chat_by_user:
                raise ValueError("No chat found.")
            return existing_chat_by_user