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
  
    def get(self, embedding_consulta: str):
     # Converter o embedding da consulta para string adequada no formato de array do PostgreSQL
        embedding_consulta_str = ','.join(map(str, embedding_consulta))

        # Consulta SQL para calcular a similaridade e retornar os top N documentos mais similares
        query = self.session.execute(f"""
            SELECT text, embedding <=> ARRAY[{embedding_consulta_str}] AS similarity
            FROM embeddings
            ORDER BY similarity
            """
        ).fetchall()
        return query

    def get_all(self) -> List[Embedding]:
        embeddings_data = self.session.query(Embedding).all()
        return embeddings_data

    def delete(self, embedding_id: str) -> None:
        embedding = self.get(embedding_id)
        self.session.delete(embedding)
        self.session.commit()
        
# def buscar_similaridade(embedding_consulta, top_n=5):
    # # Converter o embedding da consulta para string adequada no formato de array do PostgreSQL
    # embedding_consulta_str = ','.join(map(str, embedding_consulta))

    # # Consulta SQL para calcular a similaridade e retornar os top N documentos mais similares
    # query = session.execute(f"""
    #     SELECT text, embedding <=> ARRAY[{embedding_consulta_str}] AS similarity
    #     FROM embeddings
    #     ORDER BY similarity
    #