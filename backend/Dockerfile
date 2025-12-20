FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

COPY pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY app ./app

CMD ["python", "-m", "app.main"]

