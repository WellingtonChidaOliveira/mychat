from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ....infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from .user_create import UserCreate
from .....shared.middleware.token_middleware import create_token
from src.auth.application.use_cases.register import RegisterUseCase
from .....shared.infrastructure.database import get_session

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate,
                  session: Session = Depends(get_session)):
    try:
        user_repositoy = SQLAlchemyUserRepository(session)
        use_case = RegisterUseCase(user_repositoy)
        user = use_case.execute(user.username, user.email, user.password)
        token = create_token(data={"sub": user.email})
        return JSONResponse(status_code=201, content={"message": "User created successfully.", "access_token": token, "token_type": "bearer"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))