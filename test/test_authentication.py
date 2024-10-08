from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from src.login.api.authentication import router
from fastapi import FastAPI
import random
import string

app = FastAPI()

app.include_router(router)
client = TestClient(app)

@pytest.fixture
def generate_random_user():
    username = ''.join(random.sample(string.ascii_letters, 8))
    email = username + "@gmail.com"
    password = ''.join(random.sample(string.ascii_letters, 8))
    return {
        "username": username,
        "email": email,
        "password": password
    }

@pytest.fixture
def mock_db_session():
    with patch('src.login.infrastructure.database.get_session') as mock_session:
        yield mock_session

def test_register_user(mock_db_session, generate_random_user):
    payload = generate_random_user

    mock_db_session.return_value.add = lambda user: None
    mock_db_session.return_value.commit = lambda: None

    response = client.post("/register", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully."

def test_login_user(mock_db_session, generate_random_user):
    # Simulando o comportamento do banco de dados
    mock_db_session.return_value.query.return_value.filter_by.return_value.first.return_value = {
        "email": generate_random_user["email"],
        "password": generate_random_user["password"]
    }

    payload = generate_random_user
    register_response = client.post("/register", json=payload)
    assert register_response.status_code == 201

    login_payload = {
        "email": payload["email"],
        "password": payload["password"]
    }
    login_response = client.post("/login", json=login_payload)
    assert login_response.status_code == 200
    assert login_response.json()["message"] == "User logged in successfully."

    # # Simule a exclusão do usuário
    # mock_db_session.return_value.query.return_value.filter_by.return_value.delete.return_value = 1
    # delete_response = client.delete(f"/user/{payload['email']}")
    # assert delete_response.status_code == 200
    # assert delete_response.json()["message"] == "User deleted successfully."
