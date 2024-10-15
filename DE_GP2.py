#!/usr/bin/env python
# coding: utf-8

import os
import fitz  # PyMuPDF
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import psycopg2  # For PostgreSQL interaction
from openai import OpenAI

# Ensure necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Set stopwords language to Portuguese
stop_words = set(stopwords.words('portuguese'))

# Initialize OpenAI client (add your API key)
client = OpenAI(api_key='your_api_key')  # Replace with your actual API key

# Function to clean text data
def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9áàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ ]+', '', text)
    words = word_tokenize(text)
    words = [word for word in words if word not in stop_words and word.isalpha()]
    return words

# Function to split text into chunks for vectorization
def split_text_into_chunks(text, chunk_size=800, chunk_overlap=80):
    words = word_tokenize(text)
    chunks = []
    current_chunk_words = []
    for word in words:
        current_chunk_words.append(word)
        if len(current_chunk_words) >= chunk_size:
            chunks.append(' '.join(current_chunk_words[:-chunk_overlap]))
            current_chunk_words = current_chunk_words[-chunk_overlap:]
    if current_chunk_words:
        chunks.append(' '.join(current_chunk_words))
    return chunks

# Function to create embeddings using OpenAI
def create_embedding(chunk, model="text-embedding-ada-002"):
    embedding_response = client.embeddings.create(model=model, input=[chunk])
    return embedding_response.data[0].embedding

# Function to extract metadata from a PDF
def extract_pdf_metadata(pdf):
    return pdf.metadata

# Function to process a single PDF (extract text, clean it, create embeddings)
def process_pdf(pdf_file, start_page):
    pdf_file_path = os.path.join(pdf_directory, pdf_file)
    with fitz.open(pdf_file_path) as pdf:
        raw_text = ""
        all_cleaned_words = []
        for page_num in range(start_page - 1, len(pdf)):
            page = pdf.load_page(page_num)
            page_text = page.get_text()
            raw_text += page_text
            all_cleaned_words.extend(clean_text(page_text))

        cleaned_text = ' '.join(all_cleaned_words)
        chunks = split_text_into_chunks(cleaned_text)
        embeddings = [create_embedding(chunk) for chunk in chunks]

        metadata = extract_pdf_metadata(pdf)

        return cleaned_text, embeddings, metadata

# Function to insert data into PostgreSQL
def insert_data_to_postgresql(pdf_name, cleaned_text, embeddings, metadata, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pdf_data (pdf_name, cleaned_text, metadata) 
            VALUES (%s, %s, %s) RETURNING id;
        """, (pdf_name, cleaned_text, metadata))
        pdf_id = cursor.fetchone()[0]

        for embedding in embeddings:
            cursor.execute("""
                INSERT INTO pdf_embeddings (pdf_id, embedding) 
                VALUES (%s, %s);
            """, (pdf_id, embedding))

        conn.commit()
        cursor.close()

    except Exception as e:
        print(f"Error inserting data for {pdf_name}: {e}")
        conn.rollback()

# PostgreSQL connection setup
def create_postgresql_connection():
    conn = psycopg2.connect(
        host="localhost",  # Replace with your host
        database="your_database",
        user="your_user",
        password="your_password"
    )
    return conn

# Define the directory where PDFs are located
pdf_directory = 'data\\pdfs\\BCG'
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# Manually input the starting page for each PDF
starting_pages = {
    'plano-acao-adaptacao-climatica-nacional.pdf': 3,
    'plano-acao-climatica-agro.pdf': 17,
    # Add all PDFs here
}

# Establish a PostgreSQL connection
conn = create_postgresql_connection()

# Process each PDF and insert into PostgreSQL
for pdf_file in pdf_files:
    start_page = starting_pages.get(pdf_file, 1)
    cleaned_text, embeddings, metadata = process_pdf(pdf_file, start_page)
    insert_data_to_postgresql(pdf_file, cleaned_text, embeddings, metadata, conn)

# Close the PostgreSQL connection
conn.close()
