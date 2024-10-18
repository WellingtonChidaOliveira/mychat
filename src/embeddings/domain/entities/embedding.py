
from dataclasses import dataclass
import uuid
from sqlalchemy import JSON ,Column,  String
from pgvector.sqlalchemy import Vector
from ....shared.infrastructure.database import Base

@dataclass
class Embedding(Base):
    __tablename__ = "cleaned_chats"
    id= Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    pdf_name= Column(String, nullable=False)
    cleaned_text= Column(String, nullable=False)
    extra_metadata= Column(JSON, default={})
    embeddings= Column(Vector(256), nullable=False)