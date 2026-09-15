"""Rubric-based grading of a parsed, transcribed deck with Mistral Large via OpenRouter."""
from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

from .config import settings
from .context import GradingContext, default_context
from .pptx_parser import Deck

Level = Literal["ueberzeugend", "tragfaehig", "ansatzweise"]


class CriterionResult(BaseModel):
    id: str
    name: str
    level: Level
    points: float = Field(description="Points within the band of the reached level")
    max_points: float
    was_traegt: str = Field(description="What holds: concrete, with evidence (slide X, quote from the audio)")
    was_bleibt_duenn: str = Field(description="What stays thin: referring to the level descriptor")
    naechster_schritt: str = Field(description="One actionable next step")
    evidence: list[str] = Field(description="Quotes or slide references supporting the judgement")


class CoverageItem(BaseModel):
    id: str
    label: str
    status: Literal["adressiert", "teilweise", "fehlt"]
    note: str = Field(description="Where (slide) and how; for partial/missing what is missing")


class DeliveryNote(BaseModel):
    id: str
    label: str
    observation: str


class SlideNote(BaseModel):
    slide: int
    observation: str


class GradingResult(BaseModel):
    total_points: float
    max_points: float
    recommendation_identified: str = Field(description="The group's recommendation in one sentence, as pitched")
    summary: str = Field(description="Overall judgement in 3 to 5 sentences, addressed to the group")
    strengths: list[str]
    weaknesses: list[str]
    criteria: list[CriterionResult]
    coverage: list[CoverageItem]
    delivery: list[DeliveryNote]
    slide_notes: list[SlideNote]
    flags: list[str] = Field(description="What the course team should check manually")


class FormalCheck(BaseModel):
    id: str
    label: str
    ok: bool | None
    detail: str


SYSTEM = """Du bewertest als erfahrene Dozentin für Wirtschaftsinformatik einen studentischen Pitch
zu einem Teaching Case. Der Pitch liegt als vertonte PowerPoint vor: pro Folie der Folientext,
ein gerendertes Bild (falls vorhanden) und das Transkript der Tonspur.

Arbeitsweise:
- Bewerte streng entlang der Rubrik. Jedes Kriterium: erst Niveau bestimmen, dann Punkte im
  Punktband dieses Niveaus vergeben. Summe der Kriterien = total_points, nie über max_points.
- Jede Wertung braucht einen Beleg: Folie X, wörtliches Zitat aus der Tonspur oder eine Fallstelle.
  Erfinde nichts. Was nicht in Folien oder Tonspur steht, wurde nicht präsentiert.
- Unterscheide, was die Folie zeigt und was die Tonspur sagt. Sprechernotizen sind nicht Teil des
  Pitches; nutze sie nicht als Beleg für Inhalte.
- Jede Empfehlung ist zulässig. Beurteile die Begründung, nicht die Wahl.
- Prüfe die Fallbezüge gegen den Case-Text. Falsche Zahlen oder erfundene Fallstellen benennen.
- Abdeckung der Aufgaben und Vortragsqualität nur berichten, nicht bepunkten.
- Sachlich, ohne Floskeln, kein Lob ohne Beleg. Feedback ist an die Gruppe gerichtet und muss
  umsetzbar sein.
- Die Feldnamen des Ausgabeformats bleiben unverändert (level: ueberzeugend | tragfaehig |
  ansatzweise; status: adressiert | teilweise | fehlt). Die Texte in den Feldern schreibst du in
  der unten vorgegebenen Feedbacksprache."""

LANG_INSTRUCTION = {
    "de": "Feedbacksprache: Deutsch (Hochdeutsch, mit ß, nicht Schweizer Schreibweise).",
    "en": "Feedback language: English. Translate criterion names, coverage labels and delivery "
          "labels into English as well.",
}


def _deck_as_text(deck: Deck, metrics: dict) -> str:
    parts = [f"# Abgabe: {deck.source.name}",
             f"Folien: {len(deck.slides)} · vertonte Folien: {deck.narrated_slides} · "
             f"Gesamtdauer Tonspur: {metrics['total_duration_min']} min ({metrics['total_duration_s']} s) · "
             f"Sprechtempo: {metrics['words_per_minute']} Wörter/min · "
             f"Füllwörter: {metrics['filler_total']} {metrics['filler_words'] or ''}"]
    for s in deck.slides:
        dur = f"{s.audio_duration_s:.0f} s" if s.audio_duration_s else "keine Tonspur"
        parts.append(f"\n## Folie {s.number}: {s.title or '(ohne Titel)'}  [{dur}]")
        parts.append("### Folientext\n" + (s.text or "(leer)"))
        parts.append("### Transkript der Tonspur\n" + (s.transcript or "(keine Tonspur)"))
        if s.notes:
            parts.append("### Sprechernotizen (nicht Teil des Pitches)\n" + s.notes)
    return "\n".join(parts)


def formal_checks(deck: Deck, metrics: dict, rubric: dict, lang: str) -> list[FormalCheck]:
    fc = rubric.get("formal_checks", {})
    max_s = fc.get("max_duration_s")
    total = metrics["total_duration_s"]
    de = lang == "de"
    out = []
    if max_s:
        out.append(FormalCheck(
            id="duration",
            label=f"Dauer höchstens {max_s // 60} Minuten" if de else f"Duration at most {max_s // 60} minutes",
            ok=total <= max_s,
            detail=f"{metrics['total_duration_min']} min ({total} s)"))
    content_slides = [s for s in deck.slides if s.text.strip()]
    silent = [s.number for s in content_slides if not s.audio_path]
    out.append(FormalCheck(
        id="narration",
        label="Tonspur auf allen Inhaltsfolien" if de else "Narration on all content slides",
        ok=not silent,
        detail=(("alle vertont" if de else "all narrated") if not silent
                else (f"ohne Tonspur: Folien {silent}" if de else f"no narration: slides {silent}"))))
    out.append(FormalCheck(
        id="format", label="Format Voice-over-PowerPoint" if de else "Format voice-over PowerPoint", ok=True,
        detail=(f"{deck.source.suffix} mit {deck.narrated_slides} eingebetteten Tonspuren" if de
                else f"{deck.source.suffix} with {deck.narrated_slides} embedded audio tracks")))
    full = " ".join((s.text + " " + (s.transcript or "")) for s in deck.slides).lower()
    ai = any(k in full for k in ("claude", "chatgpt", "openai", "gemini", "mistral", "künstliche intelligenz bei der erstellung",
                                 "ki-einsatz", "use of ai", "generated with", "luvvoice", "elevenlabs"))
    out.append(FormalCheck(
        id="ai_disclosure",
        label="Offenlegung von KI-Einsatz bei der Erstellung" if de else "Disclosure of AI use in preparation",
        ok=None,
        detail=(("Offenlegung gefunden" if ai else "keine Offenlegung gefunden") if de
                else ("disclosure found" if ai else "no disclosure found"))))
    return out


def _build_prompt(deck: Deck, metrics: dict, ctx: GradingContext, checks: list[FormalCheck], lang: str) -> str:
    rubric, task, case = ctx.rubric, ctx.task, ctx.case
    return (
        LANG_INSTRUCTION[lang] + "\n\n" +
        "# Case-Text\n" + (case or "(kein Case-Text hinterlegt)") +
        "\n\n# Aufgabenstellung\n" + (task or "(keine Aufgabenstellung hinterlegt)") +
        "\n\n# Rubrik (YAML)\n```yaml\n" + yaml.safe_dump(rubric, allow_unicode=True, sort_keys=False) + "```\n\n" +
        "# Formale Checks (berechnet)\n" + "\n".join(f"- {c.label}: {c.detail}" for c in checks) +
        "\n\n# Sprechermetriken (berechnet)\n```json\n" + json.dumps(metrics, ensure_ascii=False, indent=1) + "\n```\n\n" +
        _deck_as_text(deck, metrics) +
        "\n\nBewerte den Pitch: alle Kriterien der Rubrik mit Niveau und Punkten, die Abdeckung jeder "
        "Aufgabe aus `coverage`, jeden Aspekt aus `delivery_aspects`, Anmerkungen je Folie und Flags. "
        + LANG_INSTRUCTION[lang]
    )


def _images(deck: Deck) -> list[tuple[int, str]]:
    return [(s.number, base64.standard_b64encode(s.image_path.read_bytes()).decode())
            for s in deck.slides if s.image_path and s.image_path.exists()]


def _grade_openrouter(prompt: str, images: list[tuple[int, str]]) -> GradingResult:
    from .openrouter import chat_json

    content: list[dict] = []
    for n, b64 in images:
        content.append({"type": "text", "text": f"Folie {n} (gerendert):"})
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
    content.append({"type": "text", "text": prompt})
    schema = GradingResult.model_json_schema()
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": content}]
    text = chat_json(messages, settings.openrouter_model, schema, "grading_result", max_tokens=16000)
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("{"):text.rfind("}") + 1]
    return GradingResult.model_validate_json(text)



def grade(deck: Deck, metrics: dict, lang: str, ctx: GradingContext | None = None) -> tuple[GradingResult, list[FormalCheck]]:
    ctx = ctx or default_context()
    checks = formal_checks(deck, metrics, ctx.rubric, lang)
    prompt = _build_prompt(deck, metrics, ctx, checks, lang)
    result = _grade_openrouter(prompt, _images(deck))
    return result, checks
