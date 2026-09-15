"""End-to-end: PPTX file -> parsed deck -> transcripts -> grading -> reports."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

from .config import settings
from .context import GradingContext, default_context
from .grader import grade
from .pptx_parser import parse_pptx
from .report import to_docx, to_markdown
from .transcribe import detect_language, speech_metrics, transcribe_deck

Progress = Callable[[str, str], None]  # (stage, message)


def run(pptx: Path, out_dir: Path, language: str = "auto", progress: Progress = lambda s, m: None,
        ctx: GradingContext | None = None) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = ctx or default_context()

    progress("parsing", "")
    deck = parse_pptx(pptx, out_dir / "work", render=settings.render_slides)

    progress("transcribing", f"{deck.narrated_slides}")
    transcribe_deck(deck)

    lang = language if language in ("de", "en") else (settings.feedback_language if settings.feedback_language in ("de", "en") else detect_language(deck))
    metrics = speech_metrics(deck, lang)
    (out_dir / "deck.json").write_text(
        json.dumps({"deck": deck.to_dict(), "metrics": metrics}, ensure_ascii=False, indent=1), encoding="utf-8")

    progress("grading", settings.mistral_model)
    result, checks = grade(deck, metrics, lang, ctx)

    progress("reporting", "")
    payload = {"language": lang, "context": ctx.summary(), "deck": deck.to_dict(), "metrics": metrics,
               "result": result.model_dump(), "formal_checks": [c.model_dump() for c in checks]}
    (out_dir / "result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    md = to_markdown(deck, metrics, result, checks, lang)
    (out_dir / "report.md").write_text(md, encoding="utf-8")
    to_docx(deck, metrics, result, checks, out_dir / "report.docx", lang)
    return {**payload, "markdown": md}
