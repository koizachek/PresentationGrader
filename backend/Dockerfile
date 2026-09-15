FROM python:3.12-slim

# ffprobe for audio durations, LibreOffice + poppler to render slides to PNG
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg libreoffice-impress poppler-utils fonts-dejavu fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml ./
RUN uv sync --no-dev --no-install-project 2>/dev/null || uv pip install --system -r pyproject.toml
COPY app ./app

ENV DATA_DIR=/data PORT=8000
VOLUME ["/data"]
EXPOSE 8000
CMD ["sh", "-c", "uv run --no-sync uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
