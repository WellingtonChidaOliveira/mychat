# Climate Action Plan Assistant

This project processes user questions related to climate action plans by embedding the question, comparing it with pre-generated document embeddings, and generating a response using OpenAI's API. It uses PostgreSQL with the pgvector extension for vector search capabilities and is containerized with Docker for easy deployment.

## Table of Contents

- [Climate Action Plan Assistant](#climate-action-plan-assistant)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Project Structure](#project-structure)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Option 1: Manual Setup](#option-1-manual-setup)
    - [Option 2: Docker Setup](#option-2-docker-setup)
  - [Running the Application with Docker](#running-the-application-with-docker)
    - [Dockerfile Overview](#dockerfile-overview)
  - [PostgreSQL with pgvector Setup](#postgresql-with-pgvector-setup)
  - [Chat Application](#chat-application)
    - [API Structure](#api-structure)
      - [1. Chat Endpoint](#1-chat-endpoint)
      - [2. Health Check Endpoint](#2-health-check-endpoint)
      - [3. Delete Chat Endpoint](#3-delete-chat-endpoint)
      - [4. Get Chat by ID Endpoint](#4-get-chat-by-id-endpoint)
      - [5. Get Chats Endpoint](#5-get-chats-endpoint)
  - [Use Cases](#use-cases)
    - [Chatbot Use Cases](#chatbot-use-cases)
    - [Embedding Use Cases](#embedding-use-cases)
  - [Usage](#usage)
    - [Example Implementation](#example-implementation)
      - [Chat Example](#chat-example)
      - [Using CleanTextUseCase](#using-cleantextusecase)
      - [Using SplitTextIntoChunksUseCase](#using-splittextintochunksusecase)
      - [Using ProcessPdfUseCase](#using-processpdfusecase)
      - [Using Embedding Model](#using-embedding-model)
  - [Environment Variables](#environment-variables)
  - [P.S](#ps)

## Description

This project implements a chatbot system using a modular architecture, capable of managing real-time interactions between users and a virtual assistant. The chatbot is designed to create, retrieve, update, and delete conversations, as well as process messages and generate responses based on embeddings, utilizing the OpenAI API.

## Project Structure

The application is divided into several main parts:

1. **FastAPI API**: Manages real-time chat interactions.
2. **Chat Repository**: Uses SQLAlchemy to persist chat data.
3. **Response Generation**: Utilizes the OpenAI API to answer questions about climate change.
4. **Text Processing**: Implements use cases for text cleaning, chunking, and creating embeddings.

## Requirements

- Python 3.x
- PostgreSQL with pgvector
- Required Python libraries:
  - numpy
  - openai
  - dotenv
  - psycopg2
  - scikit-learn
  - NLTK
  - PyMuPDF
  - pgvector
  - FastAPI

For the chat application:
- Next.js, React, and TypeScript

## Installation

### Option 1: Manual Setup

Clone the repository:

```bash
git clone https://github.com/WellingtonChidaOliveira/mychat.git
cd mychat
```

Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Configure the environment variables: Create a `.env` file in the root directory and add the following:

```
OPENAI_API_KEY=your_openai_api_key
```

### Option 2: Docker Setup

The project also provides a Docker setup for the FastAPI-based application and PostgreSQL with pgvector.

## Running the Application with Docker

To facilitate the deployment and management of the environment, we provide a Dockerfile to run the application inside a container.

### Dockerfile Overview

The Dockerfile is used to create a containerized Python application running FastAPI with the required dependencies installed. Below is the content of the Dockerfile:

```dockerfile
# Use the official Python image from Docker Hub
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./back/requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the container
COPY ./back /app

# Set environment variables (if any)
ENV PYTHONPATH=/app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## PostgreSQL with pgvector Setup

Ensure that PostgreSQL is set up with the `pgvector` extension to store and query embeddings.

## Chat Application

### API Structure

#### 1. Chat Endpoint

- **POST /ws**
  - **Description:** Allows users to send messages to the chat.
  - **Request:**
    ```json
    {
      "payload": "Your message here"
    }
    ```
  - **Headers:**
    ```
    Authorization: Bearer <your_token>
    chat_id: <chat_id>
    ```
  - **Response:** Returns the assistant's response with status 200.

#### 2. Health Check Endpoint

- **GET /health**
  - **Description:** Health check endpoint that returns the status of the API.
  - **Response:** 
    ```json
    {
      "status": "healthy"
    }
    ```

#### 3. Delete Chat Endpoint

- **DELETE /chats**
  - **Description:** Allows users to delete an existing chat.
  - **Parameters:**
    - `chat_id`: ID of the chat to be deleted in the query string.
  - **Response:** 
    ```json
    {
      "message": "Chat deleted"
    }
    ```

#### 4. Get Chat by ID Endpoint

- **GET /{chat_id}**
  - **Description:** Allows users to retrieve information about a specific chat.
  - **Parameters:**
    - `chat_id`: ID of the chat in the URL.
  - **Headers:**
    ```
    Authorization: Bearer <your_token>
    ```
  - **Response:** Returns the chat information with status 200.

#### 5. Get Chats Endpoint

- **GET /** 
  - **Description:** Allows users to retrieve all chats associated with their email.
  - **Headers:**
    ```
    Authorization: Bearer <your_token>
    ```
  - **Response:** Returns a list of chats with status 200.

## Use Cases

### Chatbot Use Cases

- **CreateChatUseCase**: Creates a new chat in the system.
- **DeleteChatUseCase**: Manages the deletion of an existing chat.
- **GetChatByIdUseCase**: Retrieves a specific chat by its ID.
- **GetChatsUseCase**: Fetches all chats associated with a user.
- **ProcessMessageUseCase**: Processes messages sent by users and generates responses.
- **UpdateChatUseCase**: Updates the information of an existing chat.

### Embedding Use Cases

1. **CleanTextUseCase**: Cleans the text by removing irrelevant words and special characters.
2. **SplitTextIntoChunksUseCase**: Divides the text into chunks for better context capture.
3. **ProcessPdfUseCase**: Processes PDF files by extracting text, cleaning it, and creating embeddings.

## Usage

### Example Implementation

#### Chat Example

```python
# Example implementation for a use case
class MyChatRepository(ChatRepository):
    pass

# Creating an instance of the repository
chat_repository = MyChatRepository()

# Creating a use case
create_chat_use_case = CreateChatUseCase(chat_repository)

# Executing the use case
chat_id = await create_chat_use_case.execute(user_email="user@example.com")
print(f"New chat created with ID: {chat_id}")
```

#### Using CleanTextUseCase

```python
from your_module import CleanTextUseCase

cleaner = CleanTextUseCase()
text = "This is an example text! Let's clean it by removing irrelevant words."
cleaned_words = cleaner.execute(text)

print("Cleaned words:", cleaned_words)
```

#### Using SplitTextIntoChunksUseCase

```python
from your_module import SplitTextIntoChunksUseCase

splitter = SplitTextIntoChunksUseCase()
text = "This is an example text that will be split into chunks."
chunks = splitter.execute(text, chunk_size=10, chunk_overlap=2)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}: {chunk}")
```

#### Using ProcessPdfUseCase

```python
from your_module import ProcessPdfUseCase

pdf_processor = ProcessPdfUseCase(pdf_directory="path/to/pdf/directory")
cleaned_text, chunk_embedding_pairs, metadata = pdf_processor.execute("example.pdf", start_page=1)

print("Cleaned text:", cleaned_text)
print("Chunk and embedding pairs:", chunk_embedding_pairs)
print("PDF metadata:", metadata)
```

#### Using Embedding Model

```python
from your_module import Embedding

# Example of creating a new Embedding instance
new_embedding = Embedding(
    pdf_name="example.pdf",
    cleaned_text="Cleaned text extracted from the PDF.",
    extra_metadata={"author": "PDF Author", "date": "2024-10-20"},
    embeddings=[0.1] * 1536  # Example of an embeddings vector
)

print("New embedding instance:", new_embedding)
```

## Environment Variables

Make sure to set the required environment variables for the application to function, such as the OpenAI API key.

## P.S
For each embedding upload in Docker, we determine a random id. So, if you carry out this process 100 times, it will be very interesting.
