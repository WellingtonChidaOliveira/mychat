import os
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import KElbowVisualizer
from openai import OpenAI
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import re
from typing import List
import asyncio

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Extrai texto de cada página
    return text

def split_text_into_chunks(text, chunk_size=512):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def generate_embeddings(text: List[str], model="text-embedding-ada-002") -> List[List[float]]:
    embeddings = []
    for chunk in text:
        response = client.embeddings.create(
            input=chunk,
            model=model,
        )
        embeddings.append(response.data[0].embedding)  # Armazena o embedding de cada chunk
    return embeddings


# Uso do código
pdf_path = "C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-adaptacao-climatica-nacional.pdf"
text = extract_text_from_pdf(pdf_path)
chunks = split_text_into_chunks(text)
embeddings = generate_embeddings(chunks)  # Chamada normal

# Agora 'embeddings' contém os embeddings para cada chunk do documento.

