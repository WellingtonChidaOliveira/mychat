from dotenv import load_dotenv
from ..chat.chat_service import ChatService
from sqlalchemy.orm import Session

load_dotenv()

class RAGModel:
    def __init__(self, session: Session):
        self.chat_service = ChatService(session)

    async def process_and_chat(self, query, old_messages):
        # Aqui você pode adicionar a lógica para processar os PDFs
        # Depois de processar, chame o chat_service para gerar a resposta
        async for response in self.chat_service.generate_response_stream(query, old_messages):
            yield response