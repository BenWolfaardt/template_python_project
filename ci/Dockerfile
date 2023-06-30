FROM python:3.11.1-slim

COPY configs /app/configs
COPY src /app/src
COPY tests /app/tests
COPY docker-compose.yml /app
COPY pyproject.toml /app
COPY README.md /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

# EXPOSE 

COPY ["ci/docker-entrypoint.sh", "/usr/local/bin/docker-entrypoint.sh"]
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
