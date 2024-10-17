

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ....application.use_cases.get_chats import GetChatsUseCase

from ....infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository

from .....shared.infrastructure.database import get_session

router = APIRouter()

@router.get("/chats")
def get_chats(user_email:str
              , session: Session = Depends(get_session)):
    try:
        chat_repository = SQLAlchemyChatRepository(session)
        use_case = GetChatsUseCase(chat_repository)
        chats = use_case.execute(user_email)
        return JSONResponse(status_code=200, content=chats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))