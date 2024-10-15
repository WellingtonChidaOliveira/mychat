from pydantic import BaseModel

class GetChats(BaseModel):
    user_email: str 
    