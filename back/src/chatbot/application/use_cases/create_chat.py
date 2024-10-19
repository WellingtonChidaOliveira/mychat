from ...domain.entities.chat import Chat
from ..interfaces.chat_repository import ChatRepository

class CreateChatUseCase:
        def __init__(self, chat_repository: ChatRepository):
                self.chat_repository = chat_repository

        async def execute(self, user_email: str):
                new_chat = Chat(user_id= user_email)
                chat = await self.chat_repository.create_chat(new_chat)
                return chat.id