from fastapi import Depends

from ...chatbot.application.use_cases.update_chat import UpdateChatHandler

from ...chatbot.application.use_cases.create_chat import CreateChatHandler

from ...chatbot.application.chat.chat_service import ChatService
from ...application.use_cases.rag_service import RAGModel
from ...infrastructure.database import get_session
from sqlalchemy.orm import Session

def get_rag_model(session: Session = Depends(get_session)):
    if not hasattr(get_rag_model, "model"):
        get_rag_model.model = RAGModel(session)
    return get_rag_model.model
