
from dataclasses import dataclass
from datetime import datetime, timezone
import uuid
from sqlalchemy import JSON, Column, DateTime, String
from ....shared.infrastructure.database import Base

@dataclass
class Chat(Base):
    __tablename__ = "chats"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()) ,index=True)
    user_id = Column(String, nullable=False)
    message = Column(JSON, default=[])
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.message = []
        self.timestamp = datetime.now(timezone.utc)
        
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message
        }
        
    def to_dict_with_partial_message(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "message": self.message[-1]["content"][:15]
        }
    
    
        
@dataclass
class Message:
    user_message: str
    bot_message: str