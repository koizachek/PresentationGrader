FROM python:3.12-slim

# ffprobe for audio durations, LibreOffice + poppler to render slides to PNG
RUN apt-get update && apt-get install -y --no-install-recommends \
        ffmpeg libreoffice-impress poppler-utils fonts-dejavu fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
# build context is the repo root; the backend lives in backend/
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv pip install --system -r pyproject.toml
COPY backend/app ./app

ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
