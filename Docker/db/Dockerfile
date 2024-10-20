FROM postgres:15

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    postgresql-server-dev-15 \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Clone and install pgvector
RUN git clone --branch v0.7.4 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make \
    && make install

# Clean up unnecessary files and packages to reduce image size
RUN apt-get purge -y --auto-remove build-essential git postgresql-server-dev-15 libc-dev

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Set the default command to run when starting the container
CMD ["postgres"]