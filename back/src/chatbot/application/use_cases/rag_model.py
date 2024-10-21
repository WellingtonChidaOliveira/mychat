# from ....shared.infrastructure.database import get_session
# from ...infrastructure.services.chat.chat_service import ChatService
# from sqlalchemy.orm import Session


# class RAGModel:
#     def __init__(self):
#         self.chat_service = ChatService()

#     async def process_and_chat(self, conversation_history):
#         async for response in self.chat_service.generate_response_stream(conversation_history):
#             yield response