import openai
from dotenv import load_dotenv
import os
import sys
import logging

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logging.error("OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

class RAGModel:
    def __init__(self):
        openai.api_key = api_key

    async def generate_response_stream(self, query):
        try:
            response = openai.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for municipal managers developing climate adaptation plans."},
                    {"role": "user", "content": query}
                ],
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