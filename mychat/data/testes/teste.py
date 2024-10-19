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
from langchain_community.document_loaders import PyPDFLoader
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

# Função para limpar o conteúdo do documento
def clean_document(document: List[str]) -> List[str]:
    return [re.sub(r'[\t\r\xa0]', '', doc.page_content).strip() for doc in document]

# Função assíncrona para carregar PDFs
async def load_pdf_async(file_path):
    loader = PyPDFLoader(file_path=file_path)
    return loader.load()

# Carregar múltiplos PDFs em paralelo
async def load_all_pdfs(file_paths):
    tasks = [load_pdf_async(file_path) for file_path in file_paths]
    return await asyncio.gather(*tasks)

# Função para gerar embeddings de forma assíncrona
async def generate_embeddings_batch(texts: List[str], model="text-embedding-ada-002", batch_size=10) -> List[np.ndarray]:
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        response = client.embeddings.create(input=batch, model=model)
        embeddings.extend([np.array(item.embedding) for item in response.data])  # Garantir que cada embedding é adicionado
    return embeddings  # Retorna uma lista de arrays

# Função de Self-Attention para extrair embeddings relevantes
class SelfAttention(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super(SelfAttention, self).__init__()
        self.attention = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)
        self.linear = nn.Linear(embed_dim, embed_dim)  # Camada adicional para refinar a saída
    
    def forward(self, embeddings):
        attn_output, _ = self.attention(embeddings, embeddings, embeddings)
        refined_output = self.linear(attn_output)  # Camada linear para refinar
        document_embedding = refined_output.mean(dim=1)  # Média das saídas
        return document_embedding

# Caminhos para os PDFs
file_paths = [
    'C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-adaptacao-climatica-nacional.pdf', 
    'C:/Users/sabrina.lopes.costa/Documents/BCG/BCG_AI/plano-acao-climatica-agro.pdf', 
    # Adicione mais caminhos conforme necessário
]

# Função principal para rodar o processo de ponta a ponta
async def main():
    # 1. Carregar PDFs
    data_nested = await load_all_pdfs(file_paths)
    data = [item for sublist in data_nested for item in sublist]  # Flatten lista
    
    # 2. Limpar dados
    cleaned_data_full = clean_document(data)
    
    # 3. Dividir texto em chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
    chunks = text_splitter.split_text(' '.join(cleaned_data_full))
    
    # 4. Criar DataFrame com os chunks
    df = pd.DataFrame(chunks, columns=["content"])
    
    # 5. Gerar embeddings para cada chunk em batches
    df["embedding"] = await generate_embeddings_batch(df["content"].tolist(), batch_size=10)

    # 6. Converter embeddings para tensor (PyTorch) usando numpy.array
    embeddings_tensor = torch.tensor(np.array(df["embedding"].tolist()), dtype=torch.float32)

    # 7. Aplicar Self-Attention
    self_attention_model = SelfAttention(embed_dim=embeddings_tensor.shape[1], num_heads=4)
    document_embeddings = self_attention_model(embeddings_tensor.unsqueeze(0))
    document_embeddings = document_embeddings.squeeze(0).detach().numpy()
        
    # 8. Normalizar os embeddings
    normalized_embeddings = normalize(document_embeddings)
    
    # 9. Determinar o número ideal de clusters com Elbow Method
    kmeans_model = KMeans()
    visualizer = KElbowVisualizer(kmeans_model, k=(2, 10))
    visualizer.fit(normalized_embeddings)
    optimal_clusters = visualizer.elbow_value_

    # 10. Aplicar K-Means com o número ideal de clusters
    kmeans = KMeans(n_clusters=optimal_clusters)
    clusters = kmeans.fit_predict(normalized_embeddings)
    
    # 11. Validar com Silhouette Score
    silhouette_avg = silhouette_score(normalized_embeddings, clusters)
    print(f"Silhouette Score para {optimal_clusters} clusters: {silhouette_avg}")
    
    # 12. Adicionar clusters ao DataFrame
    df["cluster"] = clusters
    
    # Mostrar primeiros resultados
    print(df.head())

# Rodar o processo completo
asyncio.run(main())
