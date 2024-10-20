import json
import logging
from fastapi import APIRouter, Depends,HTTPException, WebSocket, WebSocketDisconnect, status

from .....embeddings.infrastructure.database.repository.embedding_repository import SQLAlchemyEmbeddingRepository


from ....application.use_cases.get_chat_by_id import GetChatByIdUseCase
from ....application.use_cases.create_chat import CreateChatUseCase
from ....application.use_cases.process_message import ProcessMessageUseCase
from ....infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository
from ....application.use_cases.rag_model import RAGModel
from .....shared.middleware.token_middleware import get_current_user, validate_token
from .....shared.infrastructure.database import get_session
from sqlalchemy.orm import Session


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

# Carregar embeddings, cluster centers, labels, chunks e temas


@router.websocket("/ws")
async def chat(
    websocket: WebSocket,
    session: Session = Depends(get_session),
):

    await websocket.accept()
    try:
        
        token = websocket.query_params.get("token")
        chat_id = websocket.query_params.get("chat_id")
        user_email = await get_current_user(token) if validate_token(token) else None
        
        chat_repository = SQLAlchemyChatRepository(session)
        embedding_repository = SQLAlchemyEmbeddingRepository(session)
        process_message_use_case = ProcessMessageUseCase(chat_repository, embedding_repository)
        create_chat_use_case = CreateChatUseCase(chat_repository)
        get_chat_by_id_use_case = GetChatByIdUseCase(chat_repository)
        
        chat_context = []

        if user_email and chat_id:
            chat = await get_chat_by_id_use_case.execute(chat_id)     
            chat_context = [{"role": msg["role"], "content": msg["content"]} for msg in chat.message]
        elif user_email:
            chat_id = await create_chat_use_case.execute(user_email)
        else:
            # Anonymous user
            chat_id = None

        while True:
            new_message = await websocket.receive_text()
            chat_context.append({"role": "user", "content": new_message})
            
            try:
                async for response_chunk in process_message_use_case.execute(chat_id, chat_context):
                    await websocket.send_text(json.dumps({"response": response_chunk}))
                await websocket.send_text(json.dumps({"end": True}))
            except ValueError as e:
                logging.error(f"Error processing message: {str(e)}")
                await websocket.send_text(json.dumps({"error": str(e)}))
            except Exception as e:
                logging.error(f"Unexpected error processing message: {str(e)}")
                await websocket.send_text(json.dumps({"error": "An unexpected error occurred while processing your message."}))

    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error in WebSocket handler: {str(e)}")
        await websocket.close(code=status.WS_1011_INTERNAL_SERVER_ERROR)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
@router.get("/health")
async def health_check():
    return {"status": "healthy"}