from pydantic import BaseModel

class UserInteraction(BaseModel):
    payload: str