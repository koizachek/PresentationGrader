from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from . import jobs
from .config import settings
from .context import RUBRIC_EXT, TEXT_EXT, default_context

app = FastAPI(title="PresentationGrader API", version="0.1.0")


@app.on_event("startup")
def _startup() -> None:
    jobs.start_janitor()

origins = [o.strip() for o in settings.frontend_origin.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:\d+",
    allow_methods=["*"],
    allow_headers=["*"],
)

MEDIA = {
    "report.docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "report.md": "text/markdown; charset=utf-8",
    "result.json": "application/json",
}


@app.get("/api/health")
def health() -> dict:
    return {"ok": True, "model": settings.mistral_model, "transcriber": settings.transcriber,
            "transcribe_model": settings.mistral_transcribe_model,
            "report_retention_hours": settings.report_retention_hours}


@app.get("/api/config")
def config() -> dict:
    """What the grader is currently aligned to (defaults; a job may override)."""
    return {"defaults": default_context().summary(),
            "accepted": {"rubric": sorted(RUBRIC_EXT), "task": sorted(TEXT_EXT), "case": sorted(TEXT_EXT)},
            "max_upload_mb": settings.max_upload_mb}


async def _optional(upload: UploadFile | None, allowed: set[str], label: str) -> tuple[str, bytes] | None:
    if upload is None or not upload.filename:
        return None
    ext = Path(upload.filename).suffix.lower()
    if ext not in allowed:
        raise HTTPException(415, f"{label}: Dateityp {ext or '(ohne Endung)'} nicht erlaubt. Erlaubt: {', '.join(sorted(allowed))}")
    data = await upload.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"{label}: Datei größer als {settings.max_upload_mb} MB.")
    return upload.filename, data


@app.post("/api/jobs", status_code=202)
async def create_job(
    file: UploadFile = File(...),
    language: str = Form("auto"),
    rubric: UploadFile | None = File(None),
    task: UploadFile | None = File(None),
    case: UploadFile | None = File(None),
) -> dict:
    if not file.filename or not file.filename.lower().endswith(".pptx"):
        raise HTTPException(415, "Bitte eine .pptx-Datei hochladen.")
    data = await file.read()
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"Datei größer als {settings.max_upload_mb} MB.")
    if language not in ("auto", "de", "en"):
        raise HTTPException(422, "language must be auto, de or en")
    overrides = {}
    for kind, up, allowed, label in (("rubric", rubric, RUBRIC_EXT, "Rubrik"), ("task", task, TEXT_EXT, "Aufgabenstellung"),
                                     ("case", case, TEXT_EXT, "Case-Text")):
        got = await _optional(up, allowed, label)
        if got:
            overrides[kind] = got
    try:
        job = jobs.create(file.filename, data, language, overrides)
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    return job.public()


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str) -> dict:
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job nicht gefunden.")
    return job.public()


@app.get("/api/jobs/{job_id}/{name}")
def download(job_id: str, name: str) -> Response:
    job = jobs.get(job_id)
    if not job or job.status != "done":
        raise HTTPException(404, "Kein fertiger Bericht für diesen Job (oder Aufbewahrungsfrist abgelaufen).")
    blob = job.reports.get(name)
    if name not in MEDIA or blob is None:
        raise HTTPException(404, "Unbekannte Datei.")
    stem = Path(job.filename).stem
    fname = f"Bewertung {stem}{Path(name).suffix}".replace('"', "")
    return Response(content=blob, media_type=MEDIA[name],
                    headers={"Content-Disposition": f'attachment; filename="{fname}"'})
