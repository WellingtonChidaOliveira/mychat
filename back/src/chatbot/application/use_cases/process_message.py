from ...domain.entities.chat import Chat, Message
from ..interfaces.chat_repository import ChatRepository
from .rag_model import RAGModel

class ProcessMessageUseCase:
    def __init__(self, chat_repository: ChatRepository, rag_model: RAGModel):
        self.chat_repository = chat_repository
        self.rag_model = rag_model

    async def execute(self, chat_id: str, user_message: str):
        if chat_id is None:
            async for response_chunk in self.rag_model.process_and_chat(user_message):
                yield response_chunk
        else:
            chat = await self.chat_repository.get_chat_by_id(chat_id)
            response_chunks = []
            async for response_chunk in self.rag_model.process_and_chat(user_message):
                response_chunks.append(response_chunk)
                yield response_chunk
            full_response = "".join(response_chunks)
            await self.chat_repository.update_chat(chat.id, user_message, full_response)
            