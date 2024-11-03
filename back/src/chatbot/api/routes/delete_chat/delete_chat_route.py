from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .....shared.middleware.token_middleware import require_roles

from ....application.use_cases.delete_chat import DeleteChatUseCase

from ....infrastructure.database.repositories.chat_repository import SQLAlchemyChatRepository

from .....shared.infrastructure.database import get_session


router = APIRouter()

@router.delete("/chats")
def delete_chat(chat_id:str
                , session: Session = Depends(get_session),
                dependencies=[Depends(require_roles(["admin"]))]
                ):
    try:
        chat_repository = SQLAlchemyChatRepository(session)
        use_case = DeleteChatUseCase(chat_repository)
        use_case.execute(chat_id)
        return JSONResponse(status_code=200, content={"message": "Chat deleted"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))