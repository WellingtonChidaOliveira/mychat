from pytest import Session
from get_chats.get_chats_schemas import GetChats
from chatbot.infrastructure.chat_repository import ChatRepository


def __init__(self, session:Session):
            self.chat_repository = ChatRepository(session)
            
            
def get_chats(self, get_chats: GetChats):
        existing_chat_by_user = self.chat_repository.get_by_user_id(get_chats.user_email)
        if not existing_chat_by_user:
            raise ValueError("No chat found.")
        return existing_chat_by_user