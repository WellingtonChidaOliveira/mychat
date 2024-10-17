from src.chatbot.domain.entities.chat import Chat
from ..interfaces.chat_repository import ChatRepository

class DeleteChatUseCase:
    def __init__(self, chat_repository: ChatRepository):
        self.chat_repository = chat_repository
        

    def execute(self, chat_id: str, user_email: str) -> Chat:
        chat = self.chat_repository.delete_chat(chat_id, user_email)
        return chat
    
