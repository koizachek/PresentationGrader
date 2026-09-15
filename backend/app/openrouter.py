"""Thin OpenRouter client (OpenAI-compatible HTTP API), no vendor SDK."""
from __future__ import annotations

import base64
import json
from typing import Any

import httpx

from .config import settings

BASE = "https://openrouter.ai/api/v1"


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {settings.openrouter_key}",
        "HTTP-Referer": settings.frontend_origin.split(",")[0].strip() or "https://presentation-grader.vercel.app",
        "X-Title": "Presentation Grader with Voice Transcription",
        "Content-Type": "application/json",
    }


class OpenRouterError(RuntimeError):
    pass


def chat(messages: list[dict], model: str, *, response_format: dict | None = None,
         max_tokens: int = 16000, temperature: float = 0.2, timeout: float = 600) -> str:
    body: dict[str, Any] = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature}
    if response_format:
        body["response_format"] = response_format
    with httpx.Client(timeout=timeout) as c:
        r = c.post(f"{BASE}/chat/completions", headers=_headers(), json=body)
    if r.status_code != 200:
        raise OpenRouterError(f"OpenRouter {r.status_code} ({model}): {r.text[:300]}")
    data = r.json()
    if "error" in data:
        raise OpenRouterError(f"OpenRouter error ({model}): {json.dumps(data['error'])[:300]}")
    choice = data["choices"][0]
    content = choice["message"].get("content") or ""
    if isinstance(content, list):  # some providers return content parts
        content = "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return content


def chat_json(messages: list[dict], model: str, schema: dict, name: str, **kw) -> str:
    """Ask for JSON matching `schema`; falls back to json_object if the route rejects json_schema."""
    try:
        return chat(messages, model, response_format={
            "type": "json_schema", "json_schema": {"name": name, "strict": True, "schema": schema}}, **kw)
    except OpenRouterError as e:
        if "400" not in str(e) and "schema" not in str(e).lower():
            raise
        return chat(messages, model, response_format={"type": "json_object"}, **kw)


def transcribe(audio_bytes: bytes, fmt: str, model: str, language: str = "") -> str:
    lang = f" Die Sprache ist {language}." if language else ""
    content = [
        {"type": "text", "text": "Transkribiere diese Aufnahme wörtlich und vollständig. Gib nur den gesprochenen "
                                 "Text zurück, ohne Kommentare, ohne Überschrift, ohne Zeitangaben." + lang},
        {"type": "input_audio", "input_audio": {"data": base64.standard_b64encode(audio_bytes).decode(), "format": fmt}},
    ]
    return chat([{"role": "user", "content": content}], model, max_tokens=4000, temperature=0.1).strip()


def key_status() -> dict:
    if not settings.openrouter_key:
        return {"valid": False, "detail": "OPENROUTER_KEY not set"}
    try:
        with httpx.Client(timeout=20) as c:
            r = c.get(f"{BASE}/key", headers={"Authorization": f"Bearer {settings.openrouter_key}"})
        if r.status_code != 200:
            return {"valid": False, "detail": f"{r.status_code}: {r.text[:120]}"}
        d = r.json().get("data", {})
        return {"valid": True, "label": d.get("label"), "usage": d.get("usage"), "limit": d.get("limit")}
    except Exception as e:  # noqa: BLE001
        return {"valid": False, "detail": str(e)[:120]}
