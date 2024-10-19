from src.chatbot.domain.entities.chat import Chat
from ..interfaces.chat_repository import ChatRepository

class GetChatByIdUseCase:
    def __init__(self, chat_repository: ChatRepository):
                self.chat_repository = chat_repository
                
    async def execute(self, chat_id:str) -> Chat:
        chat = await self.chat_repository.get_chat_by_id(chat_id)
        return chat