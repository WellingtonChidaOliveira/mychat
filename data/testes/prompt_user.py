import numpy as np
import json  # Importa o módulo JSON
from typing import List
from mychat.data.testes.embedding_chunk import client 
from dotenv import load_dotenv
load_dotenv()

user_question = '''Se os gases de efeito estufa forem reduzidas em 80% até 2050, em relação a 1990; é possivel reverter o aumento de  2ºC até o final do século, de acordo com Intergovernmental Panel for Climate Change – IPCC (IPCC, 2014)?'''

# Carregar embeddings, cluster centers, labels, chunks e temas
data = np.load('document_data.npz', allow_pickle=True)
embeddings = data['embeddings']
cluster_centers = data['cluster_centers']
labels = data['labels']
chunks = data['chunks']
# themes = data['themes'].item()  # O item() é necessário porque temas é um dicionário

# Função para gerar o embedding da pergunta
def generate_question_embedding(question: str, model="text-embedding-ada-002") -> List[float]:
    try:
        # Gera o embedding para a pergunta usando o mesmo modelo utilizado nos chunks
        response = client.embeddings.create(input=[question], model=model)
        embedding = response.data[0].embedding  # Primeiro e único embedding da resposta
        return embedding
    except Exception as e:
        print(f"Erro ao gerar embedding da pergunta: {e}")
        return None

# Função para encontrar o cluster mais relevante com base no embedding da pergunta
def find_most_relevant_cluster(question_embedding: List[float], cluster_centers: np.ndarray) -> int:
    try:
        # Calcula a distância entre o embedding da pergunta e o centro de cada cluster (média dos embeddings)
        distances = np.linalg.norm(cluster_centers - question_embedding, axis=1)
        # Identifica o índice do cluster com a menor distância
        closest_cluster = np.argmin(distances)
        return closest_cluster
    except Exception as e:
        print(f"Erro ao encontrar o cluster mais relevante: {e}")
        return None

# Função para selecionar os Top K chunks mais relevantes do cluster escolhido
def select_top_k_chunks(cluster_indices: List[int], chunks: List[str], embeddings: List[List[float]], 
                        question_embedding: List[float], top_k: int = 5) -> List[str]:
    try:
        # Filtra os embeddings e chunks que pertencem ao cluster escolhido
        selected_embeddings = [embeddings[idx] for idx in cluster_indices]
        selected_chunks = [chunks[idx] for idx in cluster_indices]
        
        # Calcula a distância entre o embedding da pergunta e cada chunk do cluster
        distances = np.linalg.norm(np.array(selected_embeddings) - question_embedding, axis=1)
        
        # Obtém os índices dos Top K chunks mais próximos da pergunta
        top_k_indices = np.argsort(distances)[:top_k]
        
        # Retorna os chunks correspondentes aos Top K índices
        top_k_chunks = [selected_chunks[i] for i in top_k_indices]
        return top_k_chunks
    except Exception as e:
        print(f"Erro ao selecionar os Top K chunks: {e}")
        return []

# Função para gerar uma resposta com base nos chunks selecionados e reescrever usando a API da OpenAI
def generate_response(question: str, top_k_chunks: List[str]) -> str:
    try:
        # Junte os chunks para formar uma resposta inicial
        initial_response = "\n".join(top_k_chunks)

        # Faz a chamada para a API da OpenAI para reescrever a resposta
        prompt = (
            f"Você é um especialista em planos de ação climática feito para responder de forma categórica perguntas de prefeitos. "
            f"Analise essas informações e gere uma resposta para a pergunta: '{question}'. "
            f"Informações: '{initial_response}'."
            "ATENÇÃO: Utilize somente as informações fornecidas. Jamais invente informações."
            "IMPORTANTE: - Não utilize linguagem casual."
            "- Não utilize frases como: conforme as informações fornecidas, de acordo com as informações passadas e similares."
            "- Seja sucinto e direto."
        )
        openai_response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.5
        )
        rewritten_response = openai_response.choices[0].message.content.strip()
        return rewritten_response
    except Exception as e:
        print(f"Erro ao gerar a resposta: {e}")
        return None

# Função para processar a pergunta do usuário e retornar os documentos mais relevantes
def process_user_question(question: str, embeddings: List[List[float]], kmeans_labels: List[int], top_k: int = 5):
    # Gera o embedding da pergunta
    question_embedding = generate_question_embedding(question)
    
    if question_embedding:
        # Identifica o cluster mais relevante com base no embedding da pergunta
        relevant_cluster = find_most_relevant_cluster(question_embedding, cluster_centers)
        
        if relevant_cluster is not None:
            print(f"Cluster mais relevante identificado: {relevant_cluster}")
            
            # Seleciona os chunks pertencentes ao cluster mais relevante
            cluster_indices = [idx for idx, label in enumerate(kmeans_labels) if label == relevant_cluster]
            
            # Seleciona os Top K chunks mais próximos da pergunta
            top_k_chunks = select_top_k_chunks(cluster_indices, chunks, embeddings, question_embedding, top_k=top_k)

            # Gera a resposta usando a função generate_response
            response = generate_response(question, top_k_chunks)

            # Cria um dicionário para os resultados
            result = {
                "Pergunta_usuário": question,
                "Resposta": response,  # Usa a resposta gerada
                # "Tema_cluster": themes[relevant_cluster]
            }

            # Converte o dicionário em JSON
            json_result = json.dumps(result, ensure_ascii=False, indent=4)  # Formata o JSON
            print(json_result)  # Exibe o JSON
            return json_result
        else:
            print("Não foi possível identificar o cluster mais relevante.")
    else:
        print("Erro ao gerar o embedding da pergunta.")

# Chamada da função para processar a pergunta do usuário
process_user_question(user_question, embeddings, labels, top_k=5)
