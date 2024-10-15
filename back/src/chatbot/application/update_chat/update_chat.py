from pytest import Session
from .update_chat_schemas import UpdateChat
from ...infrastructure.chat_repository import ChatRepository


class UpdateChatHandler:
    def __init__(self, session:Session):
                self.chat_repository = ChatRepository(session)
                
    async def update_chat(self, chat_update: UpdateChat):
        await self.chat_repository.update_chat_in_db(chat_update.chat_id, chat_update.user_message, chat_update.bot_message)