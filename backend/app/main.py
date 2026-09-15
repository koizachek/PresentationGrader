from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from . import jobs
from .config import settings

app = FastAPI(title="PresentationGrader API", version="0.1.0")

origins = [o.strip() for o in settings.frontend_origin.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA = {
    "report.docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "report.md": "text/markdown; charset=utf-8",
    "result.json": "application/json",
    "deck.json": "application/json",
}


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "model": settings.mistral_model, "transcriber": settings.transcriber,
            "transcribe_model": settings.mistral_transcribe_model}


@app.post("/api/jobs", status_code=202)
async def create_job(file: UploadFile = File(...), language: str = Form("auto")) -> dict:
    if not file.filename or not file.filename.lower().endswith(".pptx"):
        raise HTTPException(415, "Bitte eine .pptx-Datei hochladen.")
    data = await file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Datei größer als {settings.max_upload_mb} MB.")
    if language not in ("auto", "de", "en"):
        raise HTTPException(422, "language must be auto, de or en")
    job = jobs.create(file.filename, data, language)
    return job.public()


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job nicht gefunden.")
    return job.public()


@app.get("/api/jobs/{job_id}/{name}")
def download(job_id: str, name: str) -> FileResponse:
    job = jobs.get(job_id)
    if not job or job.status != "done":
        raise HTTPException(404, "Kein fertiger Bericht für diesen Job.")
    if name not in MEDIA:
        raise HTTPException(404, "Unbekannte Datei.")
    path: Path = job.dir / name
    if not path.exists():
        raise HTTPException(404, "Datei fehlt.")
    stem = Path(job.filename).stem
    return FileResponse(path, media_type=MEDIA[name], filename=f"Bewertung {stem}{path.suffix}")
