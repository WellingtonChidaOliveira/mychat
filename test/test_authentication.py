import bcrypt
import pytest
from unittest.mock import MagicMock
from src.auth.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.auth.schemas.user_schemas import UserLogin, UserCreate
from src.auth.domain.entities.user import User
from src.auth.application.use_cases.login import LoginUseCase
from src.auth.application.use_cases.register import RegisterUseCase

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def user_service(mock_session):
    return SQLAlchemyUserRepository(mock_session)

@pytest.fixture
def login_use_case(user_service):
    return LoginUseCase(user_service)

@pytest.fixture
def register_use_case(user_service):
    return RegisterUseCase(user_service)

def test_register_user(register_use_case, user_service):
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    user_service.get_by_email = MagicMock(return_value=None)
    user_service.create = MagicMock()

    register_use_case.execute(user_create.username, user_create.email, user_create.password)

    user_service.get_by_email.assert_called_once_with("test@example.com")
    user_service.create.assert_called_once_with(User(username="testuser", email="test@example.com", hashed_password=MagicMock(), salt=MagicMock()))

def test_login_user(login_use_case, user_service):
    user_login = UserLogin(email="test@example.com", password="password123")
    salt = bcrypt.gensalt().decode('utf-8')  # Generate a valid salt
    hashed_password = bcrypt.hashpw(user_login.password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
    mock_user = User(username="user", email="test@example.com", hashed_password=hashed_password, salt=salt)
    user_service.get_by_email = MagicMock(return_value=mock_user)

    result = login_use_case.execute(user_login.email, user_login.password)

    user_service.get_by_email.assert_called_once_with("test@example.com")
    assert result == mock_user