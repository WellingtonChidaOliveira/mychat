import json
import asyncio
import websockets
from websockets import WebSocketServerProtocol
from models.rag_model import RAGModel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rag_model = None

async def chat(websocket: WebSocketServerProtocol, path: str):
    global rag_model
    if rag_model is None:
        rag_model = RAGModel()
    
    async for message in websocket:
        data = json.loads(message)
        query = data.get("message")
        
        if query:
            try:
                logging.info(f"Received query: {query}")
                async for chunk in rag_model.generate_response_stream(query):
                    logging.info(f"Sending chunk: {chunk}")
                    await websocket.send(json.dumps({"response": chunk})) 
                await websocket.send(json.dumps({"end": True}))
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                await websocket.send(json.dumps({"error": f"An error occurred: {e}"}))
        else:
            logging.warning("No query provided.")
            await websocket.send(json.dumps({"error": "No query provided."}))

async def main():
    server = await websockets.serve(chat, "localhost", 8765)
    await server.wait_closed()
    
if __name__ == "__main__":
    asyncio.run(main())