# PresentationGrader

Bewertet vertonte Studierendenpräsentationen: eine `.pptx`, in der jede Folie
eine eigene Tonspur trägt (PowerPoint „Bildschirmpräsentation aufzeichnen").
Frontend auf Vercel, Backend auf Railway.

## Ablauf

1. Upload der `.pptx` im Frontend.
2. Backend extrahiert je Folie Text, Sprechernotizen, Tonspur (MP3) und Dauer,
   rendert die Folien als PNG (LibreOffice) und transkribiert die Tonspuren.
3. Mistral Large (über OpenRouter) bewertet entlang der
   Rubrik (`backend/app/rubrics/meditec_pitch.yaml`), der Aufgabenstellung
   (`task.md`) und dem Case-Text (`case_meditec.md`). Feedbacksprache Deutsch
   oder Englisch, beim Upload wählbar oder automatisch nach der Abgabe.
4. Download der Bewertung als `.docx`, Markdown oder JSON. Kein Login.

Nichts wird gespeichert: Die Abgabe und alle hochgeladenen Dateien werden in
einem temporären Verzeichnis verarbeitet, das direkt nach der Bewertung
gelöscht wird. Die Berichte bleiben nur im Arbeitsspeicher, standardmäßig
eine Stunde (`REPORT_RETENTION_HOURS`), dann sind sie weg. Kein Volume,
keine Datenbank. Was Mistral mit den übertragenen Daten tut, regeln deren
Nutzungsbedingungen von OpenRouter und Mistral.

## Struktur

```
backend/    FastAPI + Python 3.12 (Railway, Root Directory = backend)
  app/pptx_parser.py   PPTX -> Folien, Notizen, Audio, Bilder
  app/transcribe.py    Speech-to-text mit Mistral Voxtral über OpenRouter
  app/grader.py        Bewertung mit Mistral Large über OpenRouter, strukturierter Output
  app/openrouter.py    OpenRouter-Client (HTTP, kein SDK)
  app/report.py        Markdown- und DOCX-Bericht
  app/pipeline.py      Gesamtablauf
  app/jobs.py          Job-Verwaltung im Arbeitsspeicher, temporäre Verarbeitung
  app/main.py          HTTP-API
  app/rubrics/         Rubrik (YAML), Aufgabenstellung und Case-Text (Markdown)
  scripts/run_local.py Eine Abgabe lokal bewerten
frontend/   Next.js 15 (Vercel): Upload-Feld, Fortschritt, Download
input/      Aufgabenstellung, Rubrics, Beispielabgabe (Abgaben nie committen)
```

## Rubrik

`meditec_pitch.yaml` übernimmt die vier Kriterien und Punkte aus der
Aufgabenstellung (Folie 9, 20 Punkte) und die Struktur der KI-Rubrics aus
BWL A HS26 (drei Niveaus mit Deskriptoren, typische Schwächen, Leitplanken,
formale Checks). Abdeckung der Aufgaben 1–3 und Vortragsqualität werden
berichtet, nicht bepunktet. Offene Entscheidungen stehen im Kopf der Datei.

## Lokal starten

```bash
# Backend
cd backend
cp .env.example .env            # Keys eintragen
uv sync
uv run uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
cp .env.example .env.local      # NEXT_PUBLIC_API_URL=http://localhost:8000
npm install
npm run dev
```

Eine Abgabe ohne Frontend bewerten:

```bash
cd backend
uv run python scripts/run_local.py "../input/submission/Hoffmann Christoph.pptx" ../output/hoffmann
```

Ohne LibreOffice lokal `RENDER_SLIDES=0` setzen; die Bewertung läuft dann
nur auf Text und Transkript. Ohne Transkriptionsdienst `TRANSCRIBER=notes`
(Sprechernotizen ersetzen das Transkript, nur zum Testen).

## Wiederverwendung für eine andere Aufgabe

Zwei Wege:

1. **Pro Durchlauf im Frontend** (Abschnitt „Aufgabe anpassen"): Rubrik
   (YAML/JSON), Aufgabenstellung und Case-Text (Markdown, Text, PDF, PPTX,
   DOCX) hochladen. Gilt nur für diesen Job; die Dateien werden mit dem Job
   gespeichert und im Bericht als Quelle genannt.
2. **Dauerhaft als Standard:** die drei Dateien in `backend/app/rubrics/`
   ersetzen oder über `RUBRIC_PATH`, `TASK_PATH`, `CASE_PATH` in der `.env`
   auf andere Dateien zeigen. `GET /api/config` zeigt, worauf der Grader
   gerade ausgerichtet ist.

Die Rubrik muss `max_points` und `criteria` enthalten; jedes Kriterium
`id`, `name`, `max_points` und `levels` mit `ueberzeugend`, `tragfaehig`,
`ansatzweise`. `coverage`, `delivery_aspects` und `formal_checks` sind optional.
Vorlage: `meditec_pitch.yaml`.

## API

| Methode | Pfad | Zweck |
|---|---|---|
| `GET`  | `/api/health` | Status |
| `GET`  | `/api/config` | Standard-Rubrik, -Aufgabe, -Case und erlaubte Dateitypen |
| `POST` | `/api/jobs` (multipart `file`; optional `language`=auto/de/en, `rubric`, `task`, `case`) | Abgabe hochladen, liefert Job |
| `GET`  | `/api/jobs/{id}` | Status und Ergebnis |
| `GET`  | `/api/jobs/{id}/report.docx` | Bewertung als Word |
| `GET`  | `/api/jobs/{id}/report.md` | Bewertung als Markdown |
| `GET`  | `/api/jobs/{id}/result.json` | Rohdaten |

## Deployment

**Railway (Backend):** Root Directory `backend`, baut über `backend/Dockerfile`
(mit ffmpeg, LibreOffice, poppler). Variablen: `OPENROUTER_KEY`,
`FRONTEND_ORIGIN=https://<vercel-domain>`; alle weiteren siehe `.env.example`. Kein Volume nötig.

**Vercel (Frontend):** Root Directory `frontend`, Framework Next.js.
Variable: `NEXT_PUBLIC_API_URL=https://<railway-domain>`.
