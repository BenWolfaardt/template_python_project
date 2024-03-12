FROM python:3.11.7-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        git \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=0 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN groupadd default
RUN useradd -G default appuser

RUN mkdir /app && chown -R appuser:default /app

WORKDIR /app

COPY pyproject.toml /app

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

COPY configs /app/configs
COPY .env /app
COPY src /app/src
COPY docker-compose.yml /app
COPY README.md /app

RUN find /app -type f -exec chown appuser:default {} + \
    && find /app -type d ! -path '/app/.venv*' -exec chown appuser:default {} +

COPY ["ci/app/docker-entrypoint.sh", "/usr/local/bin/docker-entrypoint.sh"]
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

USER appuser

ENTRYPOINT ["docker-entrypoint.sh"]
