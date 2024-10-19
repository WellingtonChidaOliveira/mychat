import pytest
import bcrypt
from src.auth.application.use_cases.register import RegisterUseCase
from src.auth.application.use_cases.login import LoginUseCase
from src.auth.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.auth.schemas.user_schemas import UserCreate, UserLogin
from src.auth.domain.entities.user import User, Base

@pytest.fixture(autouse=True)
def clean_database(db_session):
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()

@pytest.fixture
def user_repository(db_session):
    return SQLAlchemyUserRepository(db_session)

@pytest.fixture
def register_use_case(user_repository):
    return RegisterUseCase(user_repository)

@pytest.fixture
def login_use_case(user_repository):
    return LoginUseCase(user_repository)

def test_register_user_success(register_use_case, db_session):
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    
    result = register_use_case.execute(user_create.username, user_create.email, user_create.password)
    
    assert result.username == "testuser"
    assert result.email == "test@example.com"
    
    saved_user = db_session.query(User).filter_by(email="test@example.com").first()
    assert saved_user is not None
    assert saved_user.username == "testuser"

def test_register_user_duplicate_email(register_use_case, db_session):
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    register_use_case.execute(user_create.username, user_create.email, user_create.password)
    
    with pytest.raises(ValueError, match="User already exists"):
        register_use_case.execute("anotheruser", "test@example.com", "anotherpassword")

def test_login_user_success(register_use_case, login_use_case):
    user_create = UserCreate(username="testuser", email="test@example.com", password="password123")
    register_use_case.execute(user_create.username, user_create.email, user_create.password)
    
    result = login_use_case.execute("test@example.com", "password123")
    
    assert result.email == "test@example.com"
    assert result.username == "testuser"

def test_login_user_wrong_password(register_use_case, login_use_case):
    user_create = UserCreate(username="testuser", email="testdsad@example.com", password="dasdskajdhsak")
    register_use_case.execute(user_create.username, user_create.email, user_create.password)
    
    with pytest.raises(ValueError, match="Invalid email or password"):
        login_use_case.execute("testdsad@example.com", "wrongpassword")

def test_login_user_nonexistent(login_use_case):
    with pytest.raises(ValueError, match="Invalid email or password"):
        login_use_case.execute("nonexistent@example.com", "password123")