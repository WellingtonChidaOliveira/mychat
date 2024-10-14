from pytest import Session
from get_chat_by_id.get_chat_by_id_schemas import GetChatById
from chatbot.domain.chat import Chat
from chatbot.infrastructure.chat_repository import ChatRepository


def __init__(self, session:Session):
            self.chat_repository = ChatRepository(session)
            
async def get_chat_by_id(self, chat_get: GetChatById) -> Chat:
    chat = await self.chat_repository.get_chat_by_id(chat_get.chat_id)
    return chat