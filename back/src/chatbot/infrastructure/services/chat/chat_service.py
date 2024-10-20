import logging
import os
import numpy as np
import json  # Importa o módulo JSON
from typing import List

from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

user_question = '''Se os gases de efeito estufa forem reduzidas em 80% até 2050, em relação a 1990; é possivel reverter o aumento de  2ºC até o final do século, de acordo com Intergovernmental Panel for Climate Change – IPCC (IPCC, 2014)?'''

# Função para gerar o embedding da pergunta
def generate_question_embedding(question: str, model="text-embedding-ada-002") -> List[float]:
    try:
        # Gera o embedding para a pergunta usando o mesmo modelo utilizado nos embeddings
        response = client.embeddings.create(input=[question], model=model)
        embedding = response.data[0].embedding  # Primeiro e único embedding da resposta
        return embedding
    except Exception as e:
        print(f"Erro ao gerar embedding da pergunta: {e}")
        return None

# Função para selecionar os Top K embeddings mais relevantes baseados na distância
def select_top_k_embeddings(embeddings: List[List[float]], question_embedding: List[float], top_k: int = 5) -> List[int]:
    try:
        # Calcula a distância entre o embedding da pergunta e cada embedding dos documentos
        distances = np.linalg.norm(np.array(embeddings) - question_embedding, axis=1)

        # Obtém os índices dos Top K embeddings mais próximos da pergunta
        top_k_indices = np.argsort(distances)[:top_k]

        return top_k_indices
    except Exception as e:
        print(f"Erro ao selecionar os Top K embeddings: {e}")
        return []

# Função para gerar uma resposta com base nos embeddings selecionados e reescrever usando a API da OpenAI
def generate_response(question: str, top_k_chunks: List[str]) -> str:
    try:
        # Junte os chunks (textos) para formar uma resposta inicial
        initial_response = "\n".join(top_k_chunks)

        # Faz a chamada para a API da OpenAI para reescrever a resposta
        prompt = (
            "Seu nome é Tirica. Você é um especialista em planos de ação climática feito para responder perguntas de prefeitos."
            f"Analise essas informações e gere uma resposta para a pergunta: '{question}'. "
            f"Informações: '{initial_response}'."
            "ATENÇÃO: ê prioridade a utilizar as informações que foram fornecidas, mas você pode utilizar o seu conhecimento prévio. Jamais invente informações."
            "IMPORTANTE: - Não utilize linguagem casual."
            "- Não utilize frases como: conforme as informações fornecidas, de acordo com as informações passadas e similares."
            "- Seja sucinto e direto."
            "- Utilize majoritariamente as informações fornecidas. Jamais invente informações."
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
def process_user_question(question: str, embeddings: List[List[float]], documents: List[str], top_k: int = 5):
    # Gera o embedding da pergunta
    question_embedding = generate_question_embedding(question)
    
    if question_embedding:
        # Seleciona os Top K embeddings mais próximos da pergunta
        top_k_indices = select_top_k_embeddings(embeddings, question_embedding, top_k=top_k)

        # Recupera os chunks (textos dos documentos) correspondentes aos índices selecionados
        top_k_chunks = [documents[i] for i in top_k_indices]

        # Gera a resposta usando a função generate_response
        response = generate_response(question, top_k_chunks)

        # Cria um dicionário para os resultados
        result = {
            "Resposta": response,  # Usa a resposta gerada
        }

        # Converte o dicionário em JSON
        json_result = json.dumps(result, ensure_ascii=False, indent=4)  # Formata o JSON
        print(json_result)  # Exibe o JSON
        return json_result
    else:
        print("Erro ao gerar o embedding da pergunta.")
