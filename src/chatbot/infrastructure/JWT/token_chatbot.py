import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
import jwt
#from main import oauth2_scheme

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     try:
#         payload = jwt.decode_token(token, SECRET_KEY, algorithms=[ALGORITHM])
#         useremail: str = payload.get("sub")
#         if useremail:
#             # Save useremail in database
#             return useremail
#     except:
#         return None
    
def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

def validate_token(token: str):
    try:
        decode_token(token)
        return True
    except:
        return False
    
async def get_current_user(token: str):
    try:
        payload = decode_token(token)
        useremail: str = payload.get("sub")
        if useremail:
            # Save useremail in database
            return useremail
    except:
        return None
    