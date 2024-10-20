
import logging
from typing import Annotated

from ....application.use_cases.get_chat_by_id import GetChatByIdUseCase
from .....shared.middleware.token_middleware import get_email_from_token
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session


from ....infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository

from .....shared.infrastructure.database import get_session

router = APIRouter()

@router.get("/{chat_id}")
async def get_chat_by_id(chat_id: str, authorization:Annotated[str| None , Header()]= None
              , session: Session = Depends(get_session)):
    try:
        logging.info(f"Get chat by id: {chat_id}")
        token = authorization
        user_email = get_email_from_token(token)
        logging.info(f"User email: {user_email}")
        chat_repository = SQLAlchemyChatRepository(session)
        use_case = GetChatByIdUseCase(chat_repository)
        chat = await use_case.execute(chat_id)
        
        return JSONResponse(status_code=200, content=chat.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))