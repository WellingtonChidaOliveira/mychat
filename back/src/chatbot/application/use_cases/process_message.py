import logging
from typing import List, Dict, AsyncGenerator

from ....embeddings.application.interfaces.embedding_repository import EmbeddingRepository
from ...infrastructure.services.chat.chat_service import process_user_question
from ..interfaces.chat_repository import ChatRepository


class ProcessMessageUseCase:
    def __init__(self, chat_repository: ChatRepository, embedding_repository: EmbeddingRepository):
        self.chat_repository = chat_repository
        self.embedding_repository = embedding_repository

    async def execute(self, conversation_history: str) -> AsyncGenerator[str, None]:
        list_embeddings = self.embedding_repository.get_all()
        embeddings = [embedding.embeddings for embedding in list_embeddings]
        documents = [embedding.cleaned_text for embedding in list_embeddings]
        #logging.info(f"Embeddings: {embeddings}")
        
        full_response = process_user_question(conversation_history, embeddings=embeddings, documents=documents, top_k=5)
      
        yield full_response