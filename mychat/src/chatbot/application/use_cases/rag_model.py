from ....shared.infrastructure.database import get_session
from ...infrastructure.services.chat.chat_service import ChatService
from sqlalchemy.orm import Session


class RAGModel:
    def __init__(self):
        self.chat_service = ChatService()

    async def process_and_chat(self, query):
        # Aqui você pode adicionar a lógica para processar os PDFs
        # Depois de processar, chame o chat_service para gerar a resposta
        async for response in self.chat_service.generate_response_stream(query):
            yield response