import asyncio
import uvicorn
from fastapi import FastAPI
from src.login.api import authentication as login_auth
from src.chatbot.api import chat as websocket_chat


async def main():
    
    app = FastAPI()

    app.include_router(login_auth.router, prefix="/auth")
    app.include_router(websocket_chat.router, prefix="/chat")
    config = uvicorn.Config(app, host="localhost",port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()
        

if __name__ == "__main__":
    asyncio.run(main())
    
    