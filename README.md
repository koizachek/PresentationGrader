# PresentationGrader

Bewertet vertonte Studierendenpräsentationen: eine `.pptx`, in der jede Folie
eine eigene Tonspur trägt (PowerPoint „Bildschirmpräsentation aufzeichnen").
Frontend auf Vercel, Backend auf Railway.

## Ablauf

1. Upload der `.pptx` im Frontend.
2. Backend extrahiert je Folie Text, Sprechernotizen, Tonspur (MP3) und Dauer,
   rendert die Folien als PNG (LibreOffice) und transkribiert die Tonspuren.
3. Mistral Large bewertet entlang der
   Rubrik (`backend/app/rubrics/meditec_pitch.yaml`), der Aufgabenstellung
   (`task.md`) und dem Case-Text (`case_meditec.md`). Feedbacksprache Deutsch
   oder Englisch, beim Upload wählbar oder automatisch nach der Abgabe.
4. Download der Bewertung als `.docx`, Markdown oder JSON. Kein Login.

## Struktur

```
backend/    FastAPI + Python 3.12 (Railway, Dockerfile)
  app/pptx_parser.py   PPTX -> Folien, Notizen, Audio, Bilder
  app/transcribe.py    Speech-to-text mit Mistral Voxtral
  app/grader.py        Bewertung mit Mistral Large, strukturierter Output
  app/report.py        Markdown- und DOCX-Bericht
  app/pipeline.py      Gesamtablauf
  app/jobs.py          Job-Verwaltung (in-process)
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

## Wiederverwendung für einen anderen Case

Drei Dateien tauschen, sonst nichts: Rubrik (YAML mit `criteria`, `coverage`,
`delivery_aspects`, `formal_checks`), Aufgabenstellung (Markdown) und Case-Text
(Markdown). Pfade über `RUBRIC_PATH`, `TASK_PATH`, `CASE_PATH` in der `.env`.

## API

| Methode | Pfad | Zweck |
|---|---|---|
| `GET`  | `/api/health` | Status |
| `POST` | `/api/jobs` (multipart `file`, optional `language`=auto/de/en) | Abgabe hochladen, liefert Job |
| `GET`  | `/api/jobs/{id}` | Status und Ergebnis |
| `GET`  | `/api/jobs/{id}/report.docx` | Bewertung als Word |
| `GET`  | `/api/jobs/{id}/report.md` | Bewertung als Markdown |
| `GET`  | `/api/jobs/{id}/result.json` | Rohdaten |

## Deployment

**Railway (Backend):** Root Directory `backend`, baut über das Dockerfile
(enthält ffmpeg, LibreOffice, poppler). Variablen: `MISTRAL_API_KEY`,
`FRONTEND_ORIGIN=https://<vercel-domain>`; alle weiteren siehe `.env.example`. Ein Volume auf `/data` hält die Berichte
über Neustarts.

**Vercel (Frontend):** Root Directory `frontend`, Framework Next.js.
Variable: `NEXT_PUBLIC_API_URL=https://<railway-domain>`.
