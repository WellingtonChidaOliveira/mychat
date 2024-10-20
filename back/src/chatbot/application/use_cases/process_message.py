from typing import List, Dict, AsyncGenerator
from ...domain.entities.chat import Chat, Message
from ..interfaces.chat_repository import ChatRepository
from .rag_model import RAGModel

class ProcessMessageUseCase:
    def __init__(self, chat_repository: ChatRepository, rag_model: RAGModel):
        self.chat_repository = chat_repository
        self.rag_model = rag_model

    async def execute(self, chat_id: str | None, conversation_history: List[Dict[str, str]]) -> AsyncGenerator[str, None]:
        if not conversation_history:
            raise ValueError("Conversation history cannot be empty")

        user_message = conversation_history[-1]["content"]
        
        full_response = ""
        async for response_chunk in self.rag_model.process_and_chat(conversation_history):
            full_response += response_chunk
            yield response_chunk

        if chat_id:
            # Only update the database for authenticated users
            await self.chat_repository.update_chat(chat_id, user_message, full_response)

        # Append the assistant's response to the conversation history
        conversation_history.append({"role": "assistant", "content": full_response})