"""Minimal in-process job store. One grading run per uploaded file.

State lives in memory plus DATA_DIR/<job_id>/ on disk, which is enough for a
single Railway instance. Swap for a DB/queue if we need several workers.
"""
from __future__ import annotations

import threading
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings
from .context import GradingContext
from .pipeline import run


class Job:
    def __init__(self, filename: str, language: str = "auto", ctx: GradingContext | None = None):
        self.id = uuid.uuid4().hex[:12]
        self.filename = filename
        self.language = language
        self.ctx = ctx
        self.status = "queued"  # queued | running | done | error
        self.stage = ""
        self.message = ""
        self.error: str | None = None
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.result: dict | None = None
        self.dir: Path = settings.data_dir / self.id
        self.dir.mkdir(parents=True, exist_ok=True)

    def public(self) -> dict:
        return {
            "id": self.id, "filename": self.filename, "language": self.language, "status": self.status,
            "stage": self.stage, "message": self.message, "error": self.error,
            "created_at": self.created_at,
            "context": self.ctx.summary() if self.ctx else None,
            "result": self.result if self.status == "done" else None,
            "downloads": {
                "docx": f"/api/jobs/{self.id}/report.docx",
                "md": f"/api/jobs/{self.id}/report.md",
                "json": f"/api/jobs/{self.id}/result.json",
            } if self.status == "done" else None,
        }


_jobs: dict[str, Job] = {}
_lock = threading.Lock()


def create(filename: str, data: bytes, language: str = "auto",
           overrides: dict[str, tuple[str, bytes]] | None = None) -> Job:
    """overrides: {"rubric"|"task"|"case": (filename, bytes)}"""
    from .context import build_context

    job = Job(filename, language)
    src = job.dir / "submission.pptx"
    src.write_bytes(data)
    paths: dict[str, Path] = {}
    for kind, (name, blob) in (overrides or {}).items():
        safe = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in Path(name).name) or f"{kind}.txt"
        p = job.dir / "overrides" / kind / safe
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(blob)
        paths[kind] = p
    job.ctx = build_context(job.dir, rubric=paths.get("rubric"), task=paths.get("task"), case=paths.get("case"))
    with _lock:
        _jobs[job.id] = job
    threading.Thread(target=_work, args=(job, src), daemon=True).start()
    return job


def get(job_id: str) -> Job | None:
    return _jobs.get(job_id)


def _work(job: Job, src: Path) -> None:
    def progress(stage: str, message: str) -> None:
        job.stage, job.message = stage, message

    job.status = "running"
    try:
        job.result = run(src, job.dir, job.language, progress, job.ctx)
        job.status, job.stage, job.message = "done", "done", "Fertig"
    except Exception as e:  # noqa: BLE001
        job.status, job.stage = "error", "error"
        job.error = f"{type(e).__name__}: {e}"
        (job.dir / "error.log").write_text(traceback.format_exc(), encoding="utf-8")
