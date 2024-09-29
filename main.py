import asyncio
from api.websocket_server import main as websocket_main


if __name__ == "__main__":
    asyncio.run(websocket_main())