
# syntax=docker/dockerfile:1.7

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

# Install dependencies from PyPI
RUN pip install --no-cache-dir -r requirements.txt
# Copy application files
COPY app/ ./app/
COPY ui/ ./ui/
COPY data/ ./data/
COPY prompts/ ./prompts/
COPY docs/ ./docs/
COPY analysis/ ./analysis/
COPY eval/ ./eval/
COPY README.md .
COPY pyproject.toml .

EXPOSE 8000 8501

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
