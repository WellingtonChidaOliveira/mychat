import os
import pandas as pd
import numpy as np
import faiss
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

# Carregar o PDF e limpar o texto
loader = PyMuPDFLoader(file_path="plano-acao-adaptacao-climatica-nacional.pdf")
data = loader.load()
cleaned_text = re.sub(r'[\t\r\xa0]', '', data[0].page_content).strip()
print("Limpei os dados")

# Dividir o texto em chunks
text_splitter = NLTKTextSplitter(chunk_size=512, chunk_overlap=100)
chunks = text_splitter.split_text(cleaned_text)
print(f"Exemplo de chunk: {chunks[0]}")

# Função para gerar embeddings
def generate_embeddings(text: List[str], model="text-embedding-ada-002") -> List[float]:
    response = client.embeddings.create(
        input=text,
        model=model,
    )    
    return response.data[0].embedding

# Gerar os embeddings e criar um DataFrame
df = pd.DataFrame(chunks, columns=["content"])
df["embedding"] = df["content"].apply(lambda x: generate_embeddings([x]))

# Função para calcular a média dos embeddings de uma lista de vetores
def calculate_average_embedding(embeddings: List[List[float]]) -> List[float]:
    if not embeddings:
        return []  # Retornar uma lista vazia se não houver embeddings
    return np.mean(embeddings, axis=0)

# Calcular a média dos embeddings
df["average_embedding"] = df["embedding"].apply(lambda emb: calculate_average_embedding(emb))

# Convertendo embeddings para uma lista de vetores numpy (necessário para o FAISS)
average_embeddings = np.array(df["average_embedding"].tolist()).astype('float32')

# Inicializando o FAISS para busca vetorial
dimension = average_embeddings.shape[0]
index = faiss.IndexFlatL2(dimension)  # Indexa os vetores usando a distância Euclidiana (L2)
index.add(average_embeddings)  # Adiciona os embeddings ao índice FAISS

# Testar a busca de vizinhos mais próximos no FAISS (opcional)
D, I = index.search(average_embeddings[:1], 5)  # Busca os 5 vetores mais próximos do primeiro embedding
print(f"Vizinhos mais próximos para o primeiro chunk: {I}")

# K-Means com FAISS
n_clusters = 5  # Defina o número de clusters que deseja identificar
kmeans = faiss.Kmeans(dimension, n_clusters)
kmeans.train(average_embeddings)

# Recuperar os rótulos de cluster diretamente do KMeans
cluster_labels = kmeans.index.search(average_embeddings, 1)[1]  # Esta linha foi corrigida para evitar erro
df['cluster'] = kmeans.index.assign(average_embeddings)[1].flatten()  # Corrigir a atribuição de clusters

# Avaliar a qualidade dos clusters com o índice de silhueta
silhouette_avg = silhouette_score(average_embeddings, df['cluster'])
print(f"Índice de Silhueta: {silhouette_avg}")

# Exibir os clusters e os temas associados
print(df[['content', 'cluster']])
