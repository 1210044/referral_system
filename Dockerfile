FROM python:3.12-slim

ENV POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${POETRY_HOME}/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root --only main

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "poetry run python manage.py migrate && poetry run python manage.py collectstatic --noinput && poetry run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --worker-class gevent"]