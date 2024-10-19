import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust the import to your FastAPI app

@pytest.fixture(scope='module')
def client():
    with TestClient(app) as c:
        yield c

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.auth.domain.entities.user import Base

@pytest.fixture(scope='module')
def engine():
    return create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})

@pytest.fixture(scope='module')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()