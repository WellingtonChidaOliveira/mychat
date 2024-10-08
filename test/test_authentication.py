import string
import random
import pytest
from fastapi.testclient import TestClient
from src.login.infrastructure.database import init_db
from src.login.api.authentication import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)


# Fixture para gerar um usuário aleatório
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
    
@pytest.fixture(scope="session", autouse=True)
def initialize_database():
    init_db()


def test_register_user(generate_random_user):
    global payload 
    payload = generate_random_user
    response = client.post("/register", json=payload)
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully."

def test_login_user():
    login_payload = {
        "email": payload["email"],
        "password": payload["password"]
    }
    login_response = client.post("/login", json=login_payload)
    assert login_response.status_code == 200
    assert login_response.json()["message"] == "User logged in successfully."
    
    delete_response = client.delete(f"/user/{payload['email']}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "User deleted successfully."