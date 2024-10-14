from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
import jwt


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_HOURS = os.getenv("ACCESS_TOKEN_EXPIRE_HOURS")


def create_token(data: dict, expires_delta: timedelta):
        to_enconde = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
            
        to_enconde.update({"exp": expire})
        encoded_jwt = jwt.encode(to_enconde, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def validate_token(token: str):
    try:
        decode_token(token)
        return True
    except:
        return False
    
def get_email_from_token(token: str):
    return decode_token(token).get("sub")