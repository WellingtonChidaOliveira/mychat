import asyncio
import uvicorn
from fastapi import FastAPI
from src.shared.infrastructure.database import init_db
from src.auth.api.routes.login import login_router as login_router
from src.auth.api.routes.register import register_route as register_router
from chatbot.api.routes.chat import chat_routes as websocket_chat_router
from chatbot.api.routes.delete_chat import delete_chat_route as delete_chat_router
from chatbot.api.routes.get_chats import get_chats_route as get_chats_router
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file

init_db()

app = FastAPI()

app.include_router(login_router.router, prefix="/auth")
app.include_router(register_router.router, prefix="/auth")
app.include_router(websocket_chat_router.router, prefix="/chat")
app.include_router(delete_chat_router.router, prefix="/chat")
app.include_router(get_chats_router.router, prefix="/chat")

async def main():
    config = uvicorn.Config(app, host="localhost", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())