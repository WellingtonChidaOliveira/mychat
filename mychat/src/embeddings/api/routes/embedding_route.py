import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import openai

from ...domain.entities.embedding import Embedding

from ...application.use_cases.process_pdf import ProcessPdfUseCase
from ...infrastructure.database.repository.embedding_repository import SQLAlchemyEmbeddingRepository
from ....shared.infrastructure.database import get_session

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
# Initialize OpenAI client (add your API key)
# client = OpenAI(api_key= openai_api_key)  # Replace with your actual API key

router = APIRouter()

@router.get("/")
def embedding_data(session: Session = Depends(get_session)):
    try:
        openai.api_key = openai_api_key
        embedding_repository = SQLAlchemyEmbeddingRepository(session)
        # Manually input the starting page for each PDF

        # Define the directory where PDFs are located    
        # Caminho relativo ao diretório raiz do projeto
        pdf_directory = os.path.join(os.getcwd(), 'data', 'files', 'sustainability')
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

        embedding_use_case = ProcessPdfUseCase(pdf_directory=pdf_directory)
        starting_pages = {
            'plano-acao-adaptacao-climatica-nacional.pdf': 3,
            'plano-acao-climatica-agro.pdf': 17,
            # Add all PDFs here
        }

        # Process each PDF and insert into PostgreSQL
        for pdf_file in pdf_files:
            start_page = starting_pages.get(pdf_file, 1)
            cleaned_text, chunk_embedding_pairs, metadata = embedding_use_case.execute(pdf_file, start_page)
            #new_embedding = Embedding(pdf_name = pdf_file,cleaned_text= cleaned_text, embeddings =embeddings , extra_metadata= metadata)
            embedding_repository.create(pdf_file, chunk_embedding_pairs, metadata)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))