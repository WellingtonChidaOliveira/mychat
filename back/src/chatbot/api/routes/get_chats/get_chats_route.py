

import logging
from typing import Annotated
from .....shared.middleware.token_middleware import get_email_from_token
from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ....application.use_cases.get_chats import GetChatsUseCase

from ....infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository

from .....shared.infrastructure.database import get_session

router = APIRouter()

@router.get("/")
async def get_chats(authorization:Annotated[str| None , Header()]= None
              , session: Session = Depends(get_session)):
    try:
        token = authorization
        user_email = get_email_from_token(token)
        logging.info(f"User email: {user_email}")
        chat_repository = SQLAlchemyChatRepository(session)
        use_case = GetChatsUseCase(chat_repository)
        chats = await use_case.execute(user_email)
        
        return JSONResponse(status_code=200, content=chats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))