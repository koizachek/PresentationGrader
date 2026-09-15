"""In-memory job store. Nothing is persisted.

Each upload is processed in a temporary directory that is deleted the moment
grading finishes or fails: submission, extracted audio, rendered slides and any
uploaded task/rubric/case are gone. Only the three reports (DOCX, Markdown,
JSON) are kept, in RAM, for REPORT_RETENTION_HOURS, then dropped. No volume,
no database, nothing on disk after the run.
"""
from __future__ import annotations

import tempfile
import threading
import time
import traceback
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .config import settings
from .context import GradingContext, build_context
from .pipeline import run

REPORTS = ("report.docx", "report.md", "result.json")


class Job:
    def __init__(self, filename: str, language: str = "auto"):
        self.id = uuid.uuid4().hex[:12]
        self.filename = filename
        self.language = language
        self.status = "queued"  # queued | running | done | error
        self.stage = ""
        self.message = ""
        self.error: str | None = None
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.finished_at: float | None = None
        self.ctx: GradingContext | None = None
        self.result: dict | None = None
        self.reports: dict[str, bytes] = {}

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
    job = Job(filename, language)
    with _lock:
        _jobs[job.id] = job
    threading.Thread(target=_work, args=(job, data, overrides or {}), daemon=True).start()
    return job


def get(job_id: str) -> Job | None:
    return _jobs.get(job_id)


def _work(job: Job, data: bytes, overrides: dict[str, tuple[str, bytes]]) -> None:
    def progress(stage: str, message: str) -> None:
        job.stage, job.message = stage, message

    job.status = "running"
    try:
        with tempfile.TemporaryDirectory(prefix="grader-") as tmp:
            work = Path(tmp)
            src = work / "submission.pptx"
            src.write_bytes(data)
            paths: dict[str, Path] = {}
            for kind, (name, blob) in overrides.items():
                safe = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in Path(name).name) or f"{kind}.txt"
                p = work / "overrides" / kind / safe
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(blob)
                paths[kind] = p
            job.ctx = build_context(work, rubric=paths.get("rubric"), task=paths.get("task"), case=paths.get("case"))
            out = work / "out"
            result = run(src, out, job.language, progress, job.ctx)
            for name in REPORTS:
                job.reports[name] = (out / name).read_bytes()
            result.pop("deck", None)  # transcripts and slide text stay out of the API payload
            job.result = result
        job.status, job.stage, job.message = "done", "done", ""
    except Exception as e:  # noqa: BLE001
        job.status, job.stage = "error", "error"
        job.error = f"{type(e).__name__}: {e}"
        traceback.print_exc()
    finally:
        job.finished_at = time.time()
        del data


def purge_expired(now: float | None = None) -> int:
    hours = settings.report_retention_hours
    if not hours or hours <= 0:
        return 0
    now = now or time.time()
    with _lock:
        expired = [j.id for j in _jobs.values() if j.finished_at and now - j.finished_at > hours * 3600]
        for jid in expired:
            _jobs.pop(jid, None)
    return len(expired)


def _janitor() -> None:
    while True:
        time.sleep(300)
        try:
            purge_expired()
        except Exception:  # noqa: BLE001
            pass


def start_janitor() -> None:
    threading.Thread(target=_janitor, daemon=True).start()
