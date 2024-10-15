import logging
from .database import Base, engine
from ..domain import chat

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def init_db_chat():
    logging.info("Initializing chatbot database...")
    Base.metadata.create_all(bind=engine)
    logging.info("Chatbot database initialized.")