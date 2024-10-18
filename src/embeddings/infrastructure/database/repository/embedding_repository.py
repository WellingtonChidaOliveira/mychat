

from typing import List
from requests import Session
from ....application.interfaces.embedding_repository import EmbeddingRepository
from ....domain.entities.embedding import Embedding


class SQLAlchemyEmbeddingRepository(EmbeddingRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, embedding: Embedding) -> None:
        self.session.add(embedding)
        self.session.commit()

    def get(self, embedding_id: int) -> Embedding:
        return self.session.query(Embedding).filter(Embedding.id == embedding_id).one()

    def get_all(self) -> List[Embedding]:
        return self.session.query(Embedding).all()

    # def get_by_name(self, name: str) -> Embedding:
    #     return self.session.query(Embedding).filter(Embedding.name == name).one()

    def delete(self, embedding_id: int) -> None:
        embedding = self.get(embedding_id)
        self.session.delete(embedding)
        self.session.commit()