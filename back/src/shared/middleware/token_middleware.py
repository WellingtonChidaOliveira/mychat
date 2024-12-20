from datetime import datetime, timedelta, timezone
import os
from typing import List
from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt 


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_HOURS = os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", "1")


security = HTTPBearer()

def create_token(data: dict):
        to_encode = data.copy()
            
        expire = datetime.now(timezone.utc) + timedelta(hours=int(ACCESS_TOKEN_EXPIRE_HOURS))
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
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


    
async def get_current_user(token: str):
    try:
        payload = decode_token(token)
        useremail: str = payload.get("sub")
        if useremail:
            # Save useremail in database
            return useremail
    except:
        return None
    
def require_roles(roles: List[str]):
    def role_checker(credentials: HTTPAuthorizationCredentials = Security(security)):
        token = credentials.credentials
        decoded_token = decode_token(token)
        user_roles = decoded_token.get("roles", [])
        if not any(role in user_roles for role in roles):
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return decoded_token
    return role_checker