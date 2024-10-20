import os
import re
import time
import json
import pandas as pd
import faiss
import numpy as np
from openai import OpenAI
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor  # Para processamento paralelo
load_dotenv()

# Configuração da API
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

# Função para gerar embeddings usando a API OpenAI
def generate_embeddings(text: List[str], model="text-embedding-ada-002") -> List[float]:
    try:
        response = client.embeddings.create(input=text, model=model)
        embedding = response.data[0].embedding  # Acesso ao primeiro embedding da lista
        return embedding
    except Exception as e:
        print(f"Erro ao gerar embeddings: {e}")
        return None

# Função para salvar arquivos processados
def save_processed_files(processed_files, filepath='processed_files.json'):
    with open(filepath, 'w') as f:
        json.dump(list(processed_files), f)

# Função para carregar arquivos processados
def load_processed_files(filepath='processed_files.json'):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return set(json.load(f))
    return set()

# Função para gerar embeddings em paralelo
def generate_embeddings_parallel(chunks: List[str]) -> List[float]:
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(generate_embeddings, chunks))
    return results

# Carregar todos os documentos PDF e gerar embeddings
def process_pdfs(pdf_paths: List[str], processed_files: set):
    all_embeddings = []
    all_chunks = []
    
    for path in pdf_paths:
        try:
            # Verifica se o arquivo já foi processado
            if os.path.basename(path) in processed_files:
                print(f"Arquivo {os.path.basename(path)} já processado. Pulando...")
                continue
            print(f"Carregando documento PDF: {path}")
            loader = PyPDFLoader(file_path=path)
            data = loader.load()
            print(f"Documento {path} carregado com sucesso.")
    
            # Acessar o conteúdo textual de cada objeto Document
            document_texts = [doc.page_content for doc in data]
            
            # Dividir o texto em chunks
            print(f"Dividindo o texto em chunks para o documento: {path}")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = text_splitter.split_text(' '.join(document_texts))
            all_chunks.extend(chunks)
            print(f"Documento {path} dividido em {len(chunks)} chunks.")
    
            # Gerar embeddings em paralelo para cada chunk
            embeddings = generate_embeddings_parallel(chunks)
            embeddings = [emb for emb in embeddings if emb is not None]  # Filtrando embeddings válidos
            all_embeddings.extend(embeddings)

            # Adiciona o nome do arquivo à lista de processados
            processed_files.add(os.path.basename(path))

        except Exception as e:
            print(f"Erro ao processar o arquivo {path}: {e}")
    
    print("Todos os embeddings foram gerados.")
    return all_chunks, all_embeddings

# Função para clusterizar usando KMeans (fixando 6 clusters)
def cluster_embeddings(embeddings: List[List[float]]):
    # Padronizando os embeddings
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)
    
    # Aplicando KMeans com número de clusters fixado em 6
    start_time = time.time()
    kmeans_final = KMeans(n_clusters=6, random_state=42)
    labels = kmeans_final.fit_predict(embeddings_scaled)
    end_time = time.time()

    # Validação da clusterização com Silhouette Score
    score = silhouette_score(embeddings_scaled, labels)
    print(f"Silhouette Score: {score:.4f}")
    
    print(f"KMeans final concluído em {end_time - start_time:.2f} segundos.")
    return labels, kmeans_final.cluster_centers_

# Função para identificar o tema dos clusters e gerar o resumo diretamente
def identify_and_summarize_cluster_themes(cluster_centers, kmeans_labels, chunks, model="gpt-4o-2024-08-06"):
    themes = {}
    
    for i in range(len(cluster_centers)):
        # Seleciona os textos dos chunks que pertencem a cada cluster
        cluster_indices = [idx for idx, label in enumerate(kmeans_labels) if label == i]
        cluster_texts = [chunks[idx] for idx in cluster_indices]
        combined_text = ' '.join(cluster_texts)
        
        # Limita o tamanho do texto para evitar sobrecarregar a API
        if len(combined_text) > 10000:
            combined_text = combined_text[:10000]
        
        # Cria a mensagem para o chat completion com o prompt para identificar o tema
        messages = [
            {"role": "system", "content": "Você é um assistente útil que gera resumos de textos."},
            {"role": "user", "content": f"Identifique o tema desse pedaço de texto: {combined_text}"}
        ]
        
        try:
            # Chamada da API para gerar o resumo do tema
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=500,
                temperature=0.5
            )
            
            # Armazena o resumo gerado para o cluster atual
            summary = response.choices[0].message.content.strip()  # Aqui, usamos '.content'
            themes[i] = summary
        
        except Exception as e:
            print(f"Erro ao gerar resumo para o Cluster {i}: {e}")
            themes[i] = "Resumo não disponível"
    
    return themes


# Função para armazenar embeddings no FAISS
def store_embeddings_in_faiss(embeddings: List[List[float]], index_file: str):
    embeddings_np = np.array(embeddings).astype('float32')  # FAISS requer que os dados sejam float32
    dim = embeddings_np.shape[1]  # Dimensão dos embeddings
    
    # Criação ou atualização do índice FAISS
    if os.path.exists(index_file):
        index = faiss.read_index(index_file)
    else:
        index = faiss.IndexFlatL2(dim)  # Índice que usa distância Euclidiana
    
    index.add(embeddings_np)  # Adiciona os embeddings ao índice
    
    # Salva o índice em um arquivo
    faiss.write_index(index, index_file)
    print(f"Índice FAISS atualizado e salvo em: {index_file}")

# Função para carregar o índice FAISS
def load_embeddings_from_faiss(index_file: str):
    index = faiss.read_index(index_file)
    print(f"Índice FAISS carregado de: {index_file}")
    return index

temas = []

def display_chunks_with_themes(chunks_with_labels, cluster_themes):
    for i, (chunk, label) in enumerate(chunks_with_labels):
        theme = cluster_themes[label]  # Obtém o tema do cluster
        temas.append(f"Cluster {label}: {theme}")  # Adiciona o tema à lista
        #print(f"Chunk {i + 1}: Cluster {label} (Tema: {theme})\nTexto: {chunk[:100]}...\n")

# Exibir todos os temas identificados ao final
print("\nLista de Temas:")
print(temas)

# Lista de caminhos dos PDFs
pdf_paths = [
    'plano-enfrentamento-mudanca-climatica-nacional.pdf']
# Caminho do arquivo de índice FAISS
index_file_path = 'faiss_index.index'

# Carregar lista de arquivos processados
processed_files = load_processed_files()

# Verifica se o arquivo de índice já existe
if os.path.exists(index_file_path):
    # Carrega o índice se já existe
    index = load_embeddings_from_faiss(index_file_path)
else:
    # Processar PDFs e obter chunks e embeddings
    chunks, embeddings = process_pdfs(pdf_paths, processed_files)

    # Clusterizar os embeddings
    if embeddings:
        labels, cluster_centers = cluster_embeddings(embeddings)
    
        print("Iniciando armazenamento no FAISS...")
        start_time = time.time()

        store_embeddings_in_faiss(embeddings, index_file_path)

        end_time = time.time()
        print(f"Armazenamento FAISS concluído em {end_time - start_time:.2f} segundos.")

        # Identificar temas dos clusters e gerar resumos diretamente
        themes = identify_and_summarize_cluster_themes(cluster_centers, labels, chunks)
        print("Temas identificados para cada cluster:")
        for cluster_id, theme in themes.items():
            print(f"Cluster {cluster_id}: {theme}")

        # Adicionar labels aos chunks
        chunks_with_labels = list(zip(chunks, labels))

        # Exibir os resultados com temas
        display_chunks_with_themes(chunks_with_labels, themes)  # Exibe os chunks com temas
    
    # Salvar lista de arquivos processados
    save_processed_files(processed_files)
# Salvando embeddings, cluster centers, labels, chunks e temas
    np.savez('document_data.npz', embeddings=embeddings, cluster_centers=cluster_centers, labels=labels, chunks=chunks, themes=themes)
