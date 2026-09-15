"""Speech-to-text for the per-slide audio tracks.

Provider is chosen with TRANSCRIBER:
  mistral : Mistral Voxtral transcription endpoint.
  notes   : no STT; speaker notes stand in for the transcript (dev/fallback).
"""
from __future__ import annotations

import re
from pathlib import Path

from .config import settings
from .pptx_parser import Deck

FILLERS = {
    "de": ["ähm", "äh", "ehm", "hm", "quasi", "sozusagen", "halt", "irgendwie", "genau"],
    "en": ["um", "uh", "erm", "like", "you know", "basically", "actually", "sort of", "kind of"],
}
_DE = {"und", "der", "die", "das", "nicht", "ist", "wir", "mit", "für", "auch", "eine", "sich"}
_EN = {"and", "the", "is", "not", "we", "with", "for", "also", "this", "that", "are", "of"}

MIME = {".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".mp4": "audio/mp4", ".wav": "audio/wav",
        ".aac": "audio/aac", ".wma": "audio/x-ms-wma", ".m4v": "video/mp4"}


def _mistral_transcribe(path: Path) -> str:
    from mistralai.client import Mistral

    client = Mistral(api_key=settings.mistral_api_key, server=settings.mistral_server)
    kwargs = {"language": settings.transcribe_language} if settings.transcribe_language else {}
    r = client.audio.transcriptions.complete(
        model=settings.mistral_transcribe_model,
        file={"file_name": path.name, "content": path.read_bytes(),
              "content_type": MIME.get(path.suffix.lower(), "application/octet-stream")},
        **kwargs,
    )
    return r.text or ""



_PROVIDERS = {"mistral": _mistral_transcribe}


def transcribe_deck(deck: Deck, provider: str | None = None) -> Deck:
    provider = provider or settings.transcriber
    if provider not in _PROVIDERS and provider != "notes":
        raise ValueError(f"Unknown TRANSCRIBER={provider!r} (mistral | notes)")
    for s in deck.slides:
        if not s.audio_path:
            s.transcript = None
        elif provider == "notes":
            s.transcript = s.notes
        else:
            s.transcript = _PROVIDERS[provider](s.audio_path).strip()
        s.word_count = len(s.transcript.split()) if s.transcript else 0
    return deck


def detect_language(deck: Deck) -> str:
    """'de' or 'en' from slide text + transcripts (crude stopword vote)."""
    words = re.findall(r"[a-zäöüß]+", " ".join(s.text + " " + (s.transcript or "") for s in deck.slides).lower())
    de = sum(w in _DE for w in words)
    en = sum(w in _EN for w in words)
    return "en" if en > de else "de"


def speech_metrics(deck: Deck, lang: str = "de") -> dict:
    words = sum(s.word_count for s in deck.slides)
    secs = deck.total_audio_s
    full = " ".join(s.transcript or "" for s in deck.slides).lower()
    fillers = {f: len(re.findall(rf"\b{re.escape(f)}\b", full)) for f in FILLERS.get(lang, FILLERS["de"])}
    fillers = {k: v for k, v in fillers.items() if v}
    per_slide = [
        {"slide": s.number, "duration_s": s.audio_duration_s, "words": s.word_count,
         "wpm": round(s.word_count / s.audio_duration_s * 60) if s.audio_duration_s else None}
        for s in deck.slides
    ]
    return {
        "language": lang,
        "total_duration_s": round(secs, 1),
        "total_duration_min": round(secs / 60, 1),
        "total_words": words,
        "words_per_minute": round(words / secs * 60) if secs else None,
        "filler_words": fillers,
        "filler_total": sum(fillers.values()),
        "per_slide": per_slide,
    }
