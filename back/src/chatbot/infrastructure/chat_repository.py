import logging
from fastapi import logger
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from ..domain.chat import Chat

class ChatRepository:
    def __init__(self, session: Session):
        self.session = session

    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    async def create_chat(self, chat: Chat) -> Chat:
        #chat = Chat(user_id= user_id)
        self.session.add(chat)
        self.session.commit()
        self.session.refresh(chat)
        return chat
        
    def get_by_user_id(self, user_id: str) -> Chat:
        return self.session.query(Chat).filter(Chat.user_id == user_id)
    
    def delete_chat(self, chat_id: int, useremail: str):
        chat = self.session.query(Chat).filter(Chat.id == chat_id and Chat.user_id == useremail).first()
        self.session.delete(chat)
        self.session.commit()
        
    async def update_chat_in_db(self, chat_id: int, user_message: str, bot_response: str):
        chat = self.session.query(Chat).filter(Chat.id == chat_id).first()
        if chat:
            chat.message.append({"role": "user", "content": user_message})
            chat.message.append({"role": "assistant", "content": bot_response})
            flag_modified(chat, "message")
            self.session.commit()
        else:
            logger.error(f"Chat with id {chat_id} not found in database")
            
    async def get_chat_by_id(self, chat_id: str) -> Chat:
        try: 
            return self.session.query(Chat).filter(Chat.id == chat_id).first()
        except Exception as e:
            logger.error(f"Error in get_chat_by_id: {e}")
            raise 