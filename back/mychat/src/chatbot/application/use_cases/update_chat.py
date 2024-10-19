from ..update_chat.update_chat_schemas import UpdateChat
from ..interfaces.chat_repository import ChatRepository


class UpdateChatUseCase:
    def __init__(self, chat_repository: ChatRepository):
                self.chat_repository = chat_repository
                
    async def update_chat(self, chat_update: UpdateChat):
        await self.chat_repository.update_chat_in_db(chat_update.chat_id, chat_update.user_message, chat_update.bot_message)