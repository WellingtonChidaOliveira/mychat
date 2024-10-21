import os
import openai
import logging
from dotenv import load_dotenv
from sqlalchemy.orm import Session

# from data.testes.embedding_chunk import cluster_embeddings
from ...application.use_cases.process_pdf import ProcessPdfUseCase
from ...infrastructure.database.repository.embedding_repository import SQLAlchemyEmbeddingRepository
from ....shared.infrastructure.database import get_session, init_db

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Inicializar o banco de dados
init_db()

# Obter uma sessão do banco de dados
session: Session = next(get_session())

try:
    # Configurar a chave da API OpenAI
    openai.api_key = openai_api_key
    embedding_repository = SQLAlchemyEmbeddingRepository(session)

    # Definir o diretório onde os PDFs estão localizados
    pdf_directory = os.path.join(os.getcwd(), 'data', 'files', 'sustainability')
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

    embedding_use_case = ProcessPdfUseCase(pdf_directory=pdf_directory)
    starting_pages = {
        'plano-acao-adaptacao-climatica-nacional.pdf': 3,
        'plano-acao-climatica-agro.pdf': 17,
        # Adicione todos os PDFs aqui
    }

    # Processar cada PDF e inserir no PostgreSQL
    total_files = len(pdf_files)
    for index, pdf_file in enumerate(pdf_files, start=1):
        logging.info(f"Processando PDF {index}/{total_files} ({(index/total_files)*100:.2f}%)")
        start_page = starting_pages.get(pdf_file, 1)
        cleaned_text, chunk_embedding_pairs, metadata = embedding_use_case.execute(pdf_file, start_page)
        #summary = cluster_embeddings(chunk_embedding_pairs)
        embedding_repository.create(pdf_file, chunk_embedding_pairs, metadata)

    print("PDFs processados com sucesso")

except ValueError as e:
    print(f"Erro ao processar PDFs: {e}")