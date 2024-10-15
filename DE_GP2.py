#!/usr/bin/env python
# coding: utf-8

# In[4]:


pip install langchain


# In[5]:


get_ipython().system('pip install nltk')


# In[6]:


get_ipython().system('pip install PyMuPDF')


# In[7]:


get_ipython().run_line_magic('pip', 'install -qU pypdf')


# In[8]:


pip install --upgrade langchain


# In[9]:


pip show langchain


# In[10]:


import sys
print(sys.version)


# In[11]:


pip install langchain-community


# In[48]:


from langchain_community.document_loaders import PyMuPDFLoader
import re
import nltk
import fitz  # PyMuPDF
import os
nltk.download('stopwords')
from nltk.corpus import stopwords
import pymupdf


# In[50]:


# Define the directory where your PDFs are located
pdf_directory = 'C:\\Users\\Michael.Linker\\OneDrive - Fortive\\Documents\\BCG'

# List all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Iterate over the list of PDF files and load each one
for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_directory, pdf_file)
    loader = PyMuPDFLoader(pdf_file_path)  # Initialize the loader with the file path
    data = loader.load()  # Load the data

    # 'data' now contains the loaded content from the PDF file.
    # Here you can process 'data' as needed, for example, print it or save it for further processing.
    print(f"Contents of {pdf_file}:")
    print(data)
    # Add any additional processing or saving of 'data' here.


# In[51]:


pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Now you can iterate over the list of PDF files and print them
for pdf_file in pdf_files:
    print(pdf_file)


# In[60]:


# Initialize an empty dictionary for starting pages
starting_pages = {}

# Manually input the starting page for each PDF
starting_pages['plano-acao-adaptacao-climatica-nacional.pdf'] = 3  # Replace '2' with the correct starting page
starting_pages['plano-acao-climatica-agro.pdf'] = 17  # Replace '2' with the correct starting page
starting_pages['plano-acao-climatica-curitiba.pdf'] = 9  # Replace '2' with the correct starting page
starting_pages['plano-acao-climatica-federal.pdf'] = 7  # Replace '2' with the correct starting page
starting_pages['plano-acao-climatica-itabirito.pdf'] = 16  # Replace '2' with the correct starting page
starting_pages['plano-acao-climatica-joao-pessoa.pdf'] = 14  # Replace '2' with the correct starting page
starting_pages['plano-acao-climatica-sp-regiao.pdf'] = 5  # Replace '2' with the correct starting page
starting_pages['plano-enfrentamento-mudanca-climatica-nacional.pdf'] = 1  # Replace '2' with the correct starting page


# In[54]:


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

# Ensure you have the necessary NLTK data
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Set the language for stopwords to Portuguese
stop_words = set(stopwords.words('portuguese'))

# Example function to clean text data
def clean_text(text):
    # Remove unwanted characters (keep only letters, numbers and accents)
    text = re.sub(r'[^a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]+', '', text)
    # Tokenize the text to words
    words = word_tokenize(text)
    # Remove stopwords
    words = [word for word in words if word not in stop_words]
    # Remove non-alphabetic characters and keep accents
    words = [word for word in words if word.isalpha() or word in ['á', 'à', 'â', 'ã', 'é', 'è', 'ê', 'í', 'ï', 'ó', 'ô', 'õ', 'ö', 'ú', 'ç', 'ñ', 'Á', 'À', 'Â', 'Ã', 'É', 'È', 'Ê', 'Í', 'Ï', 'Ó', 'Ô', 'Õ', 'Ö', 'Ú', 'Ç', 'Ñ']]
    return words


# In[56]:


# Initialize dictionaries to hold the raw and cleaned content of each PDF
pdf_raw_contents = {}
pdf_cleaned_contents = {}


# In[62]:


# List all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Iterate over the list of PDF files
for pdf_file in pdf_files:
    pdf_file_path = os.path.join(pdf_directory, pdf_file)
    # Open the PDF file
    with fitz.open(pdf_file_path) as pdf:
        # Get the starting page number for the current file
        start_page = starting_pages.get(pdf_file, 1)  # Default to 1 if not specified
        raw_text = ""
        all_cleaned_words = []  # Use a list to collect all cleaned words
        # Iterate over each page in the PDF, starting from the specified page
        for page_num in range(start_page - 1, len(pdf)):  # start_page - 1 because PyMuPDF is 0-indexed
            page = pdf.load_page(page_num)
            page_text = page.get_text()
            raw_text += page_text
            # Clean the text and extend the list of cleaned words
            all_cleaned_words.extend(clean_text(page_text))

        # Store the raw text content in the dictionary
        pdf_raw_contents[pdf_file] = raw_text
        # Store the cleaned words in the dictionary, converting the list of words back to a string
        pdf_cleaned_contents[pdf_file] = ' '.join(all_cleaned_words)


# In[64]:


# Assuming pdf_cleaned_contents is a dictionary with the cleaned contents of each PDF
# Get the first PDF filename from the list of keys in the dictionary
first_pdf_filename = next(iter(pdf_cleaned_contents))

# Print the filename
print(f"Contents of the first PDF ({first_pdf_filename}):")

# Print the cleaned text of the first PDF
print(pdf_cleaned_contents[first_pdf_filename])


# In[ ]:


get_ipython().system('pip install openai')


# In[ ]:


from langchain.text_splitter import NLTKTextSplitter


# In[ ]:


from nltk.tokenize import word_tokenize

# Define a function to split text into chunks of approximately 800 tokens with an overlap of 80 tokens
def split_text_into_chunks(text, chunk_size=800, chunk_overlap=80):
    words = word_tokenize(text)
    chunks = []
    current_chunk_words = []

    for word in words:
        current_chunk_words.append(word)
        if len(current_chunk_words) >= chunk_size:
            chunks.append(' '.join(current_chunk_words[:-chunk_overlap]))
            current_chunk_words = current_chunk_words[-chunk_overlap:]
    chunks.append(' '.join(current_chunk_words))  # Add the last chunk
    return chunks

# Define a function to create embeddings for a chunk of text using the OpenAI API
def create_embedding(chunk, model="text-embedding-ada-002"):
    embedding_response = client.embeddings.create(
        model=model,
        input=[chunk]
    )
    return embedding_response.data[0].embedding


# In[ ]:


import openai

# Initialize the client with your API key
from openai import OpenAI

# Instantiate the OpenAI client with your API key directly
client = OpenAI(
  api_key=''  # Replace with your actual API key
)
# Instantiate the OpenAI client with your API key

# Create an embedding for a piece of text using the specified embedding model
embedding_response = client.embeddings.create(
    model="text-embedding-ada-002",  # Replace with the model you want to use
    input=["The quick brown fox jumps over the lazy dog"]  # Replace with the text you want to embed
)

# Extract the embedding vector
embedding_vector = embedding_response.data[0].embedding

# Print the embedding vector
print(embedding_vector)


# In[ ]:


from nltk.tokenize import word_tokenize
from openai import OpenAI

# Define a function to split text into chunks of approximately 800 tokens with an overlap of 80 tokens
def split_text_into_chunks(text, chunk_size=800, chunk_overlap=80):
    words = word_tokenize(text)
    chunks = []
    current_chunk_words = []

    for word in words:
        current_chunk_words.append(word)
        if len(current_chunk_words) >= chunk_size:
            chunks.append(' '.join(current_chunk_words[:-chunk_overlap]))
            current_chunk_words = current_chunk_words[-chunk_overlap:]
    if current_chunk_words:  # Add the last chunk if it's not empty
        chunks.append(' '.join(current_chunk_words))
    return chunks

# Define a function to create embeddings for a chunk of text using the OpenAI API
client = OpenAI(
  api_key=''  # Replace with your actual API key
)

def create_embedding(chunk, model="text-embedding-ada-002"):
    embedding_response = client.embeddings.create(
        model=model,
        input=[chunk]
    )
    return embedding_response.data[0].embedding

# Assuming you have a dictionary `pdf_cleaned_contents` with cleaned text for each PDF
pdf_embeddings = {}

for pdf_name, cleaned_text in pdf_cleaned_contents.items():
    # Split the cleaned text into chunks
    chunks = split_text_into_chunks(cleaned_text)

    # Create embeddings for each chunk
    embeddings = [create_embedding(chunk) for chunk in chunks]

    # Store the embeddings in the dictionary
    pdf_embeddings[pdf_name] = embeddings

# Now 'pdf_embeddings' is a dictionary where the keys are PDF filenames and the values are lists of embeddings


# In[ ]:


# Print embeddings for each PDF
for pdf_name, embeddings in pdf_embeddings.items():
    print(f"Embeddings for {pdf_name}:")
    for i, embedding in enumerate(embeddings):
        # Print only the first 2 embeddings for brevity
        if i < 2:
            print(f"  Chunk {i+1} embedding (first 10 values): {embedding[:10]}")
    print("\n")  # Add a newline for better readability between PDFs


# In[ ]:


get_ipython().system('pip install psycopg2-binary numpy')


# In[ ]:


get_ipython().system('pip install psycopg')


# In[ ]:


get_ipython().system('pip install pgvector')


# In[ ]:


get_ipython().system('pip install asyncpg')


# In[ ]:


import psycopg2
from psycopg2.extras import execute_values
from pgvector.psycopg import register_vector_async


# In[ ]:


# Step 1: Import required libraries
import psycopg2
import psycopg
import numpy as np
import json
import asyncpg


# In[ ]:


connection_string = "postgresql://myuser:mypassword@localhost:3000/chatbot_db"


# In[ ]:


conn = psycopg2.connect(connection_string)
cur = conn.cursor()


# In[ ]:


await register_vector_async(conn)


# In[ ]:


table_create_command = """
CREATE TABLE IF NOT EXISTS
    embeddings (
    id bigserial primary key, 
    content text,
    metadata json,
    embedding vector(768) --Verificar tamanho do vetor
    )
;
"""


# In[ ]:


get_ipython().system('jupyter nbconvert --to script config_template.ipynb')

