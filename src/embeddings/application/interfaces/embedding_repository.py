
from abc import ABC, abstractmethod
from typing import List, Optional

from ...domain.entities.embedding import Embedding


class EmbeddingRepository(ABC):
    @abstractmethod
    def get(self, embedding_id: str) -> Optional[Embedding]:
        pass

    @abstractmethod
    def get_all(self, embedding_ids: List[str]) -> List[Embedding]:
        pass

    @abstractmethod
    def create(self, embedding: Embedding):
        pass

    @abstractmethod
    def delete(self, embedding_id: str):
        pass