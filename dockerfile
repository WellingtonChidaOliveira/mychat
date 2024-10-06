FROM postgres:15

RUN apt-get update && \
    apt-get install -y postgresql-server-dev-all git build-essential && \
    git clone --branch v0.7.4 https://github.com/pgvector/pgvector.git && \
    cd pgvector && make && make install

COPY init.sql /docker-entrypoint-initdb.d/
