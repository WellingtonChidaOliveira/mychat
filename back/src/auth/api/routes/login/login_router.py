
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ....infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from .....shared.middleware.token_middleware import create_token
from .....shared.infrastructure.database import get_session
from src.auth.application.use_cases.login import LoginUseCase
from .user_login import UserLogin


router = APIRouter()


# def get_chat_service(session: Session = Depends(get_session)):
#     return session


@router.post("/login")
def login_user(user_login: UserLogin
               , session: Session = Depends(get_session)):
    try:
        user_repository = SQLAlchemyUserRepository(session)
        use_case = LoginUseCase(user_repository)
        user = use_case.execute(user_login.email, user_login.password)
        token = create_token(data={"sub": user.email})
        return JSONResponse(status_code=200, content={"access_token": token, "token_type": "bearer"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))