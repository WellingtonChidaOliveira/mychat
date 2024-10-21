import json
import logging
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .....embeddings.infrastructure.database.repository.embedding_repository import SQLAlchemyEmbeddingRepository
from ....application.use_cases.get_chat_by_id import GetChatByIdUseCase
from ....application.use_cases.create_chat import CreateChatUseCase
from ....application.use_cases.process_message import ProcessMessageUseCase
from ....infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository
from .....shared.middleware.token_middleware import get_current_user, validate_token
from .....shared.infrastructure.database import get_session

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

class UserInteraction(BaseModel):
    payload: str

@router.post("/ws")
async def chat(
    request: Request,
    user_interaction: UserInteraction,
    session: Session = Depends(get_session),
):
    try:
        token = request.headers.get("authorization")
        chat_id = request.headers.get("chat_id")
        user_email = await get_current_user(token) if validate_token(token) else None
        if not user_email:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
        chat_repository = SQLAlchemyChatRepository(session)
        embedding_repository = SQLAlchemyEmbeddingRepository(session)
        process_message_use_case = ProcessMessageUseCase(chat_repository, embedding_repository)
       
        response = [chunk async for chunk in process_message_use_case.execute(user_interaction.payload)]
        
        return JSONResponse(status_code=200, content={"assistant": response})

    except Exception as e:
        logging.error(f"Unexpected error in WebSocket handler: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@router.get("/health")
async def health_check():
    return {"status": "healthy"}