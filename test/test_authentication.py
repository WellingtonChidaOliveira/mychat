import pytest
import random
import string
import logging
from sqlalchemy import text

logger = logging.getLogger(__name__)

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

def test_register_user(client, generate_random_user, db_session):
    payload = generate_random_user

    logger.debug(f"Attempting to register user: {payload}")
    
    # Check if the users table exists
    result = db_session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='users';"))
    if result.fetchone():
        logger.debug("users table exists")
    else:
        logger.error("users table does not exist")
    
    response = client.post("/auth/register", json=payload)

    # Log the response for debugging
    logger.debug(f"Response status code: {response.status_code}")
    logger.debug(f"Response content: {response.content}")

    # Verifications
    assert response.status_code == 201, f"Expected status code 201, but got {response.status_code}"
    assert response.json()["message"] == "User created successfully."