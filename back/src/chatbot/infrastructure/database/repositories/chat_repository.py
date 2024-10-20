import logging
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from src.chatbot.application.interfaces.chat_repository import ChatRepository
from ....domain.entities.chat import Chat

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SQLAlchemyChatRepository(ChatRepository):
    def __init__(self, session: Session):
        self.session = session

    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    async def create_chat(self, chat: Chat) -> Chat:
        self.session.add(chat)
        self.session.commit()
        self.session.refresh(chat)
        return chat
        
    def get_by_user_id(self, user_id: str) -> List[dict]:
        chats = self.session.query(Chat).filter(Chat.user_id == user_id).all()
        if not chats:
            logging.info(f"No chats found for user_id {user_id}")
        else:
            logging.info(f"Chats for user_id {user_id}: {chats}")
        return [chat.to_dict() for chat in chats]
    
    def delete_chat(self, chat_id: int, useremail: str):
        chat = self.session.query(Chat).filter(Chat.id == chat_id and Chat.user_id == useremail).first()
        self.session.delete(chat)
        self.session.commit()
        return chat
        
    async def update_chat(self, chat_id: int, user_message: str, bot_response: str) -> Chat:
        chat = self.session.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            chat.message.append({"role": "user", "content": user_message})
            chat.message.append({"role": "assistant", "content": bot_response})
            flag_modified(chat, "message")
            self.session.commit()
            return chat
        else:
            logging.error(f"Chat with id {chat_id} not found in database")
            
    async def get_chat_by_id(self, chat_id: str) -> Chat:
        try: 
            return self.session.query(Chat).filter(Chat.id == chat_id).first()
        except Exception as e:
            logging.error(f"Error in get_chat_by_id: {e}")
            raise 