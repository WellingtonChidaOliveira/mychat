# Climate Action Plan Assistant

This project processes user questions related to climate action plans by embedding the question, comparing it with pre-generated document embeddings, and generating a response using OpenAI's API. It uses PostgreSQL with the `pgvector` extension for vector search capabilities and is containerized with Docker for easy deployment.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Docker Setup](#docker-setup)
- [Running the Application with Docker](#running-the-application-with-docker)
- [PostgreSQL with pgvector Setup](#postgresql-with-pgvector-setup)
- [Chat Application](#chat-application)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Requirements

- Python 3.x
- PostgreSQL with `pgvector`
- Required Python libraries:
  - `numpy`
  - `openai`
  - `dotenv`
  - `psycopg2`
  - `scikit-learn`
  - `Next.js`, `React`, and `TypeScript` for the chat application

## Installation

### Option 1: Manual Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/climate-action-assistant.git
    cd climate-action-assistant
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**:
    Create a `.env` file in the root directory and add the following:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

### Option 2: Docker Setup

The project also provides a Docker setup for the FastAPI-based application and PostgreSQL with `pgvector`.

### Running the Application with Docker

To make it easier to deploy and manage the environment, we provide a `Dockerfile` to run the application inside a container.

#### Dockerfile Overview

The Dockerfile is used to create a containerized Python application running FastAPI with the required dependencies installed. Below is the Dockerfile content:

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
