from typing import List, Dict, AsyncGenerator

from ....embeddings.application.interfaces.embedding_repository import EmbeddingRepository
from ...infrastructure.services.chat import process_user_question
from ..interfaces.chat_repository import ChatRepository


class ProcessMessageUseCase:
    def __init__(self, chat_repository: ChatRepository, embedding_reposiotry: EmbeddingRepository):
        self.chat_repository = chat_repository
        self.embedding_reposiotry = embedding_reposiotry

    async def execute(self, chat_id: str | None, conversation_history: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        list_embeddings = self.embedding_reposiotry.get_all()
        data = [embedding.embeddings for embedding in list_embeddings]
        embeddings = data['embeddings']
        labels = data['labels']
        
        if not conversation_history:
            raise ValueError("Conversation history cannot be empty")

        user_message = conversation_history[-1]["content"]
        
        full_response = ""
        full_response =  process_user_question(conversation_history, embeddings=embeddings, kmeans_labels=labels, top_k=5)

        if chat_id:
            # Only update the database for authenticated users
            await self.chat_repository.update_chat(chat_id, user_message, full_response)
            
        return full_response
       