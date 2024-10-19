from typing import List
from sqlalchemy.orm import Session
from ....application.interfaces.embedding_repository import EmbeddingRepository
from ....domain.entities.embedding import Embedding
import uuid
import json
import numpy as np

class SQLAlchemyEmbeddingRepository(EmbeddingRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, pdf_name: str, chunk_embedding_pairs: List[tuple], metadata: dict) -> None:
        for chunk, embedding in chunk_embedding_pairs:
            embedding_array = np.array(embedding, dtype=np.float32)
            new_embedding = Embedding(
                id=str(uuid.uuid4()),
                pdf_name=pdf_name,
                cleaned_text=chunk,
                extra_metadata=json.dumps(metadata),
                embeddings=embedding_array
            )
            self.session.add(new_embedding)
        self.session.commit()

    def get(self, embedding_id: str) -> Embedding:
        return self.session.query(Embedding).filter(Embedding.id == embedding_id).one()

    def get_all(self) -> List[Embedding]:
        return self.session.query(Embedding).all()

    def delete(self, embedding_id: str) -> None:
        embedding = self.get(embedding_id)
        self.session.delete(embedding)
        self.session.commit()