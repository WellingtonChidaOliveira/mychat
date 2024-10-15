import openai
from dotenv import load_dotenv
import os
import sys
import logging
from sqlalchemy.orm import Session

from ...domain.chat import Chat

from ...infrastructure.chat_repository import ChatRepository

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

class ChatService:
    def __init__(self, session:Session):
            openai.api_key = api_key
            self.chat_repository = ChatRepository(session)

    async def generate_response_stream(self, query, old_messages):
        try:
            messages = old_messages if old_messages else []
            messages.append({"role": "system", "content": "You are a helpful assistant for municipal managers developing climate adaptation plans."})
            messages.append({"role": "user", "content": query})
            response = openai.chat.completions.create(
                messages= messages,
                model="gpt-4",
                stream=True,
            )
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                if content:
                    yield content
        except Exception as e:
            logging.error(f"Error in generate_response_stream: {e}")
            raise
        