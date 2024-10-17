import bcrypt
import pytest
from unittest.mock import MagicMock
from src.login.application.interfaces.user_service import UserService
from src.login.schemas.user_schemas import UserLogin, UserCreate
from src.login.domain.entities.user import User

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def user_service(mock_session):
    return UserService(mock_session)

def test_register_user(user_service):
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    user_service.user_repository.get_by_email = MagicMock(return_value=None)
    user_service.user_repository.add = MagicMock()

    user_service.register(user_create)

    user_service.user_repository.get_by_email.assert_called_once_with("test@example.com")
    user_service.user_repository.add.assert_called_once()

def test_login_user(user_service):
    user_login = UserLogin(email="test@example.com", password="password123")
    salt = bcrypt.gensalt().decode('utf-8')  # Gerar um salt válido
    password = bcrypt.hashpw(user_login.password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')
    mock_user = User(username="user", email="test@example.com",hashed_password=password, salt=salt)
    user_service.user_repository.get_by_email = MagicMock(return_value=mock_user)

    user_service.login(user_login)

    user_service.user_repository.get_by_email.assert_called_once_with("test@example.com")