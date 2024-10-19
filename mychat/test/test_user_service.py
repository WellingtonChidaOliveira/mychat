import pytest
import sqlalchemy.exc
from src.auth.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.auth.schemas.user_schemas import UserLogin, UserCreate
from src.auth.domain.entities.user import User, Base
from src.auth.application.use_cases.login import LoginUseCase
from src.auth.application.use_cases.register import RegisterUseCase

@pytest.fixture(autouse=True)
def clean_database(db_session):
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()


@pytest.fixture
def user_repository(db_session):
    return SQLAlchemyUserRepository(db_session)

def test_register_user(user_repository):
    user = User(username="testuser", email="test@test.com", hashed_password="password", salt="salt")
    user_repository.create(user)
    fetched_user = user_repository.get_by_email("test@test.com")
    
    assert fetched_user.username == "testuser"
    assert fetched_user.email == "test@test.com"
    #assert fetched_user.hashed_password != "password"  # Ensure password is hashed

def test_get_email_user_not_exists(user_repository):
    user = user_repository.get_by_email("test@test.com")
    assert user is None

@pytest.mark.parametrize("missing_field", ["email", "username", "hashed_password"])
def test_create_user_with_missing_field(user_repository, missing_field, db_session):
    user_data = {
        "username": "testuser",
        "email": "test@test.com",
        "hashed_password": "password",
        "salt": "salt"
    }
    del user_data[missing_field]
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        user_repository.create(User(**user_data))
    db_session.rollback()
    

def test_create_user_with_existing_email(user_repository,db_session):
    user_repository.create(User(username="testuser1", email="test@test.com", hashed_password="password", salt="salt"))
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        user_repository.create(User(username="testuser2", email="test@test.com", hashed_password="password", salt="salt"))
    db_session.rollback()

def test_create_user_with_existing_username(user_repository, db_session):
    user_repository.create(User(username="testuser", email="test1@test.com", hashed_password="password", salt="salt"))
    with pytest.raises(sqlalchemy.exc.IntegrityError):
        user_repository.create(User(username="testuser", email="test2@test.com", hashed_password="password", salt="salt"))
    db_session.rollback()

