FROM python:3.8.3-alpine AS base

ENV PYTHON_UNBUFFERED=1 \
    PYTHON_FAULTHANDLER=1

RUN apk add --no-cache libressl libffi libxml2 libxslt


FROM base AS builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.0.0 \
    POETRY_VIRTUALENVS_PATH=/venv/

RUN apk add --no-cache --virtual .build-deps \
    gcc g++ libressl-dev libffi-dev libxml2-dev libxslt-dev \
    && pip install "poetry==$POETRY_VERSION"
    # && apk del --no-cache .build-deps

COPY pyproject.toml poetry.lock /

RUN poetry install --no-dev --no-interaction --no-ansi \
    && rm -rf ~/.cache/


FROM base AS build

COPY --from=builder /venv /venv
COPY *.py /app/
COPY ffdl/ /app/ffdl/

EXPOSE 4444

WORKDIR /app/

CMD /venv/*/bin/python server.py
