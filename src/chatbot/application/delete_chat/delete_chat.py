from pytest import Session
from delete_chat.delete_chat_schemes import DeleteChat
from chatbot.domain.chat import Chat
from ...infrastructure.chat_repository import ChatRepository


def __init__(self, session:Session):
    self.chat_repository = ChatRepository(session)
        

def delete_chat_handler(self, user_delete: DeleteChat):
    chat = self.chat_repository.delete_chat(user_delete.chat_id, user_delete.user_email)
    return chat
    
