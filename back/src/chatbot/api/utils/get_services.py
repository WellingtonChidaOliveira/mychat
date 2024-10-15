from fastapi import Depends

from ...application.update_chat.update_chat import UpdateChatHandler

from ...application.create_chat.create_chat import CreateChatHandler

from ...application.chat.chat_service import ChatService
from ...application.rag.rag_service import RAGModel
from ...infrastructure.database import get_session
from sqlalchemy.orm import Session

def get_rag_model(session: Session = Depends(get_session)):
    if not hasattr(get_rag_model, "model"):
        get_rag_model.model = RAGModel(session)
    return get_rag_model.model

def get_chat_service(session: Session = Depends(get_session)):
    return ChatService(session)

def get_chat_service_update(session: Session = Depends(get_session)):
    return UpdateChatHandler(session)

def get_chat_service_create(session: Session = Depends(get_session)):
    return CreateChatHandler(session)