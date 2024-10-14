import logging
import json
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, WebSocket, WebSocketDisconnect, status

from ..application.update_chat.update_chat_schemas import UpdateChat

from ..application.create_chat.create_chat_schema import CreateChat

from ..application.create_chat.create_chat import CreateChatHandler
from ..application.update_chat.update_chat import UpdateChatHandler
from .utils.get_services import get_chat_service, get_chat_service_create, get_chat_service_update, get_rag_model
from ..application.chat.chat_service import ChatService
from ..infrastructure.JWT.token_chatbot import get_current_user, validate_token
from ..infrastructure.database import get_session
from ..application.rag.rag_service import RAGModel
from sqlalchemy.orm import Session

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


router = APIRouter()

@router.websocket("/ws")
async def chat(
    websocket: WebSocket, 
    rag_model: Annotated[RAGModel, Depends(get_rag_model)],
    chat_service: Annotated[ChatService, Depends(get_chat_service)],
    update_chat_service: Annotated[UpdateChatHandler, Depends(get_chat_service_update)],
    create_chat_service: Annotated[CreateChatHandler, Depends(get_chat_service_create)],
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    
    await websocket.accept()
    try:
        token = None
        chatId = None
        for header_name, header_value in websocket.headers.items():
            if header_name.lower() == "authorization":
                token = header_value.split(" ")[1]
            elif header_name.lower() == "chatid":
                chatId = header_value
                
        logging.info(f"Token: {token}")
            
        useremail = None
        old_messages = None
        if(validate_token(token)):
            useremail = await get_current_user(token)
        if useremail and chatId is None:
            chat = await create_chat_service.create_chat_handler(CreateChat(email=useremail))
            chatId = chat.id
            logging.info(f"Chat created with id: {chatId}")
        elif useremail and chatId:
            chat = await chat_service.get_chat_by_id(chat_id=chatId)
            logging.info(f"Chat already exists with id: {chat.id}")
            old_messages = chat.message

        
        while True:
            full_response = ""
            logging.info("Waiting for message...")
            data = await websocket.receive_text()
            logging.info(f"Received data: {data}")
            async for response in rag_model.process_and_chat(data, old_messages=old_messages):
                logging.info(f"Response chunk: {response}")
                await websocket.send_text(json.dumps({"response": response}))
                full_response += response
            # Enviar mensagem de finalização
            await websocket.send_text(json.dumps({"end": True}))
            if useremail and chatId:
                await update_chat_service.update_chat(UpdateChat(chat_id=chatId,user_message= data, bot_message=full_response))
    except WebSocketDisconnect:
        logging.info("WebSocket disconnected")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@router.get("/health")
async def health_check():
    return {"status": "healthy"}