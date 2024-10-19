import os
import pandas as pd
import numpy as np
import faiss
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from openai import OpenAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import NLTKTextSplitter
import re
from typing import List
from dotenv import load_dotenv
import nltk

nltk.download('punkt')
load_dotenv()

# Configuração da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("A chave da API OpenAI não foi encontrada. Verifique se a variável de ambiente está configurada corretamente.")
client = OpenAI(api_key=OPENAI_API_KEY)

# Função para limpar o conteúdo dos PDFs
def clean_document(document: List[str]) -> List[str]:
    return [re.sub(r'[\t\r\xa0]', '', doc.page_content).strip() for doc in document]

# Função para gerar embeddings usando a API OpenAI
def generate_embeddings(text: List[str], model="text-embedding-ada-002") -> List[float]:
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding

# Função para calcular a média dos embeddings de uma lista de vetores
def calculate_average_embedding(embeddings: List[List[float]]) -> List[float]:
    if not embeddings:
        return []  # Retornar uma lista vazia se não houver embeddings
    return np.mean(embeddings, axis=0)

# Carregar todos os documentos PDF
pdf_paths = ['C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-adaptacao-climatica-nacional.pdf','C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-climatica-agro.pdf']
all_chunks = []
for path in pdf_paths:
    loader = PyMuPDFLoader(file_path=path)
    data = loader.load()
    cleaned_data = clean_document(data)

    # Dividir o texto em chunks
    text_splitter = NLTKTextSplitter(chunk_size=512, chunk_overlap=100)
    chunks = text_splitter.split_text(' '.join(cleaned_data))
    all_chunks.extend(chunks)

# Vetorizar os chunks de texto
df = pd.DataFrame(all_chunks, columns=["content"])
df["embedding"] = df["content"].apply(lambda x: generate_embeddings([x]))

# **1. Abordagem K-Means para identificar os temas**
n_clusters = 5  # Defina o número de clusters, ajustável conforme os documentos
X = np.array(df["embedding"].tolist()).astype('float32')

# Aplicar o K-Means
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df['cluster'] = kmeans.fit_predict(X)

# Avaliar a qualidade dos clusters com o índice de silhueta
silhouette_avg = silhouette_score(X, df['cluster'])
print(f"Índice de Silhueta: {silhouette_avg}")

# **2. Abordagem de Média dos Vetores**
df["average_embedding"] = df["embedding"].apply(lambda emb: calculate_average_embedding(emb))

# **3. Similaridade usando FAISS**
dimension = X.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(X)  # Adicionar embeddings ao índice

# Função para buscar respostas similares
def find_similar_responses(query, top_k=5):
    query_embedding = generate_embeddings([query])
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)

    # Procurar os chunks mais similares
    D, I = faiss_index.search(query_embedding, top_k)
    return df.iloc[I.flatten()]

# Simulação de consulta do usuário
query = "Quais são os projetos de sustentabilidade no nível federal?"
result = find_similar_responses(query)
print(result[["content", "cluster"]])

