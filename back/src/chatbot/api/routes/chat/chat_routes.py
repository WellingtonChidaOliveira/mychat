import json
import logging
from .....shared.middleware.rate_limit_middleware import RateLimiter
from fastapi import APIRouter, Depends,HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi_limiter import FastAPILimiter

from .....shared.utils.get_services import Utils

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


@router.websocket("/ws")
async def chat(
    websocket: WebSocket,
    session: Session = Depends(get_session),
):
    await websocket.accept()
    try:
        rate_limite = RateLimiter(max_requests=10, time_window=60)
        client_ip = websocket.client.host

        # Rate limiting logic: Allow up to 10 messages per 60 seconds
        if not await rate_limite.is_allowed(client_ip, 3, 60):
            await websocket.send_text(json.dumps({"error": "Rate limit exceeded. Please wait before sending more messages."}))
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        
        token = Utils.get_header(websocket=websocket, header_name="authorization")
        chat_id = Utils.get_header(websocket=websocket, header_name="chatid")
        user_email = await get_current_user(token) if validate_token(token) else None
        
        chat_repository = SQLAlchemyChatRepository(session)
        rag_model = RAGModel()
        process_message_use_case = ProcessMessageUseCase(chat_repository, rag_model)
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