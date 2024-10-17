import json
import logging
from fastapi import APIRouter, Depends,HTTPException, WebSocket, WebSocketDisconnect, status

from ....shared.utils.get_services import Utils

from ...application.use_cases.get_chat_by_id import GetChatByIdUseCase
from ...application.use_cases.create_chat import CreateChatUseCase
from ...application.use_cases.process_message import ProcessMessageUseCase
from ...infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository
from ...application.use_cases.rag_model import RAGModel
from ....shared.middleware.token_middleware import get_current_user, validate_token
from ....shared.infrastructure.database import get_session
from sqlalchemy.orm import Session


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()


@router.websocket("/ws")
async def chat(
    websocket: WebSocket,
    session: Session = Depends(get_session)
):
    await websocket.accept()
    try:
        token = Utils.get_header(websocket=websocket, header_name="authorization")
        chat_id = Utils.get_header(websocket=websocket, header_name="chatid")
        user_email = await get_current_user(token) if validate_token(token) else None
        logging.info(f"Token: {user_email}")
        
        chat_repository = SQLAlchemyChatRepository(session)
  
        rag_model = RAGModel()
        process_message_use_case = ProcessMessageUseCase(chat_repository, rag_model)
        create_chat_use_case = CreateChatUseCase(chat_repository)
        get_chat_by_id_use_case = GetChatByIdUseCase(chat_repository)
        chat_context = []

        if user_email and not chat_id:
            logging.info("Creating chat")
            chat = await create_chat_use_case.execute(user_email)
            chat_id = chat
        elif user_email and chat_id:
            logging.info("Getting chat")
            chat = await get_chat_by_id_use_case.execute(chat_id)
            logging.info(f"Can get chat: {chat.user_id}")
            chat_context = chat.message
            
        while True:
            new_message = await websocket.receive_text()
            chat_context.append({"role": "user", "content": new_message})
                
            async for response in process_message_use_case.execute(chat_id, json.dumps(chat_context)):
                await websocket.send_text(json.dumps({"response": response}))
            await websocket.send_text(json.dumps({"end": True}))

    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/health")
async def health_check():
    return {"status": "healthy"}