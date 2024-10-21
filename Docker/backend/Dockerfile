# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
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

# Command to run the embedding populate script and then start the application
CMD ["sh", "-c", "PYTHONPATH=/app python3 -m src.embeddings.api.routes.embedding_populate && uvicorn main:app --host 0.0.0.0 --port 8000"]