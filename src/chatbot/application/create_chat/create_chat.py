from pytest import Session

from .create_chat_schema import CreateChat
from ...domain.chat import Chat
from ...infrastructure.chat_repository import ChatRepository

class CreateChatHandler:
        def __init__(self, session:Session):
                self.chat_repository = ChatRepository(session)

        async def create_chat_handler(self, create_user: CreateChat):
                new_chat = Chat(user_id= create_user.email)
                chat = await self.chat_repository.create_chat(new_chat)
                return chat