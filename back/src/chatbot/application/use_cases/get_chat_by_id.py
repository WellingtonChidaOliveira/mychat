import logging
from src.chatbot.domain.entities.chat import Chat
from ..interfaces.chat_repository import ChatRepository

class GetChatByIdUseCase:
    def __init__(self, chat_repository: ChatRepository):
                self.chat_repository = chat_repository
                
    async def execute(self, chat_id:str) -> Chat:
        logging.info(f"Get chat by id: {chat_id}")
        chat = await self.chat_repository.get_chat_by_id(chat_id)
        if not chat:
            raise ValueError("No chat found.")
        return chat