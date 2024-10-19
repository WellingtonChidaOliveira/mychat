import os
from  openai import OpenAI
from ...application.use_cases.clean_text import CleanTextUseCase
from ...application.use_cases.split_text_into_chunks import SplitTextIntoChunksUseCase
import fitz  # PyMuPDF
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')


client = OpenAI(api_key= openai_api_key)  # Replace with your actual API key
class ProcessPdfUseCase:
    def __init__(self, pdf_directory: str):
        self.pdf_directory = pdf_directory
        
    def create_embedding(self, chunk, model="text-embedding-ada-002"):
        embedding_response = client.embeddings.create(model=model, input=[chunk])
        return embedding_response.data[0].embedding 

    # Function to extract metadata from a PDF
    def extract_pdf_metadata(self, pdf):
        return pdf.metadata

    # Function to process a single PDF (extract text, clean it, create embeddings)
    def execute(self, pdf_file, start_page):
        clean_text_use_case = CleanTextUseCase()
        split_text_into_chunks_use_case = SplitTextIntoChunksUseCase()
        
        pdf_file_path = os.path.join(self.pdf_directory, pdf_file)
        with fitz.open(pdf_file_path) as pdf:
            raw_text = ""
            all_cleaned_words = []
            for page_num in range(start_page - 1, len(pdf)):
                page = pdf.load_page(page_num)
                page_text = page.get_text()
                raw_text += page_text
                cleaned_texts = clean_text_use_case.execute(page_text)
                all_cleaned_words.extend(cleaned_texts)

            cleaned_text = ' '.join(all_cleaned_words)
            chunks = split_text_into_chunks_use_case.execute(cleaned_text)
            chunk_embedding_pairs = [(chunk, self.create_embedding(chunk)) for chunk in chunks]

            metadata = self.extract_pdf_metadata(pdf)

            return cleaned_text, chunk_embedding_pairs, metadata