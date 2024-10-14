from pydantic import BaseModel

class DeleteChat(BaseModel):
    chat_id: str 
    user_email: str