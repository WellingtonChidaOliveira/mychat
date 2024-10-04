import logging
import json
from fastapi import APIRouter, HTTPException, WebSocket
from ..application.rag_service import RAGModel

# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

rag_model = None

router = APIRouter()

@router.websocket("/ws")
async def chat(websocket: WebSocket):
    global rag_model
    if rag_model is None:
        rag_model = RAGModel()
    await websocket.accept()
    try:
        while True:
            logging.info("Waiting for message...")
            data = await websocket.receive_text()
            logging.info(f"Received data: {data}")
            async for response in rag_model.process_and_chat(data):
                logging.info(f"Response chunk: {response}")
                await websocket.send_text(json.dumps({"response": response}))
            # Enviar mensagem de finalização
            await websocket.send_text(json.dumps({"end": True}))
    except Exception as e:
        await websocket.close()
        raise HTTPException(status_code=400, detail=str(e))