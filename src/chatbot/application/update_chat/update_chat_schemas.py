from pydantic import BaseModel

class UpdateChat(BaseModel):
    chat_id: str
    user_message: str
    bot_message: str
    