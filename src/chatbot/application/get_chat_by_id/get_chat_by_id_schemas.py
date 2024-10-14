from pydantic import BaseModel

class GetChatById(BaseModel):
    chat_id: str 
    