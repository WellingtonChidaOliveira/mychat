from pydantic import BaseModel

class CreateChat(BaseModel):
    email: str 