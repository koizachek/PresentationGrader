"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { API, LEVEL_LABEL, fetchConfig, fetchJob, uploadSubmission, type Config, type Job, type Overrides } from "@/lib/api";
import { Help } from "./help";

type Lang = "auto" | "de" | "en";

const STAGES: Record<string, string> = {
  queued: "In Warteschlange",
  parsing: "Folien, Notizen und Tonspuren werden extrahiert",
  transcribing: "Tonspuren werden transkribiert (Voxtral)",
  grading: "Bewertung wird erstellt (Mistral Large)",
  reporting: "Bericht wird geschrieben",
  done: "Fertig",
  error: "Fehler",
};

const HELP = {
  upload: "Erwartet wird eine PowerPoint-Datei (.pptx), in der jede Folie eine eigene Tonspur trägt, wie sie PowerPoint mit „Bildschirmpräsentation aufzeichnen“ erzeugt. Text, Notizen und Audio werden pro Folie ausgelesen. Maximale Dateigröße 200 MB. Die Datei wird nach der Bewertung gelöscht.",
  language: "Sprache des Feedbacks. „Automatisch“ richtet sich nach der Sprache der Abgabe. Die Bewertungskriterien bleiben dieselben.",
  grade: "Startet die Pipeline: Folien extrahieren, Tonspuren transkribieren, entlang der Rubrik bewerten, Bericht erzeugen. Dauert je nach Länge einige Minuten. Kein Login, nichts wird über den Bericht hinaus gespeichert.",
  result: "Vier Kriterien aus der Aufgabenstellung, zusammen 20 Punkte. Je Kriterium wird erst das Niveau bestimmt (überzeugend, tragfähig, ansatzweise), dann die Punkte im Band dieses Niveaus. Jede Wertung nennt Belege aus Folien oder Tonspur.",
  download: "Die vollständige Bewertung als Word-Datei zum Weitergeben. Markdown und JSON enthalten dieselben Inhalte für die Weiterverarbeitung.",
  coverage: "Ob die Teilaufgaben 1 bis 3 im Pitch vorkommen. Wird berichtet, nicht bepunktet: Der Pitch verlangt die beste Lösung, nicht alle Teilaufgaben.",
  delivery: "Beobachtungen zur Tonspur: Sprechtempo, Verständlichkeit, Verhältnis von Folie und gesprochenem Wort, Dauer. Wird berichtet, nicht bepunktet.",
  formal: "Automatisch geprüft: Dauer gegenüber der 7-Minuten-Vorgabe, Tonspur auf allen Inhaltsfolien, Dateiformat, Offenlegung von KI-Einsatz. Nur Hinweise, kein Abzug.",
  context: "Der Grader ist standardmäßig auf die unten genannte Aufgabe ausgerichtet. Für eine andere Aufgabe laden Sie hier eigene Dateien hoch; sie gelten nur für diesen Durchlauf. Rubrik als YAML oder JSON im Format der Standardrubrik (Kriterien mit id, name, max_points und drei Niveaus). Aufgabenstellung und Case-Text als Markdown, Text, PDF, PPTX oder DOCX.",
  rubric: "Bewertungsraster: Kriterien, Punkte je Kriterium, Niveau-Deskriptoren, optional Abdeckungs-Checks und Vortragsaspekte. Ohne Upload gilt die Standardrubrik.",
  task: "Die Aufgabenstellung, die die Studierenden bekommen haben. Das Modell prüft daran, ob der Pitch die gestellte Frage beantwortet.",
  case: "Das Fallmaterial (Teaching Case), auf das sich die Abgabe bezieht. Damit prüft das Modell Zahlen und Fallbezüge.",
};

export default function Page() {
  const [file, setFile] = useState<File | null>(null);
  const [lang, setLang] = useState<Lang>("auto");
  const [job, setJob] = useState<Job | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [drag, setDrag] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const [config, setConfig] = useState<Config | null>(null);
  const [ov, setOv] = useState<Overrides>({});
  const ovRefs = { rubric: useRef<HTMLInputElement>(null), task: useRef<HTMLInputElement>(null), case: useRef<HTMLInputElement>(null) };

  useEffect(() => { fetchConfig().then(setConfig).catch(() => setConfig(null)); }, []);

  const maxMb = config?.max_upload_mb ?? 200;

  const pick = (f: File | undefined) => {
    setError(null);
    if (!f) return;
    if (!f.name.toLowerCase().endsWith(".pptx")) { setError("Bitte eine .pptx-Datei wählen."); return; }
    if (f.size > maxMb * 1024 * 1024) { setError(`Datei ist ${(f.size / 1024 / 1024).toFixed(0)} MB groß, erlaubt sind maximal ${maxMb} MB.`); return; }
    setFile(f); setJob(null);
  };

  const submit = useCallback(async () => {
    if (!file) return;
    setBusy(true); setError(null);
    try { setJob(await uploadSubmission(file, lang, ov)); }
    catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    finally { setBusy(false); }
  }, [file, lang, ov]);

  useEffect(() => {
    if (!job || job.status === "done" || job.status === "error") return;
    const t = setInterval(async () => {
      try { setJob(await fetchJob(job.id)); }
      catch (e) { setError(e instanceof Error ? e.message : String(e)); }
    }, 2500);
    return () => clearInterval(t);
  }, [job]);

  const running = job && (job.status === "queued" || job.status === "running");
  const res = job?.status === "done" ? job.result?.result : null;
  const checks = job?.status === "done" ? job.result?.formal_checks ?? [] : [];

  return (
    <main>
      <h1>Presentation Grader with Voice Transcription</h1>
      <p className="sub">Vertonte Präsentation hochladen, Bewertung als Word-Datei herunterladen.</p>

      <section className="card">
        <h2>1. Abgabe <Help text={HELP.upload} /></h2>
        <label
          className={`drop ${drag ? "active" : ""}`}
          onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
          onDragLeave={() => setDrag(false)}
          onDrop={(e) => { e.preventDefault(); setDrag(false); pick(e.dataTransfer.files[0]); }}
        >
          <input ref={inputRef} type="file" accept=".pptx" onChange={(e) => pick(e.target.files?.[0])} />
          <div><strong>{file ? file.name : "Datei hier ablegen oder klicken"}</strong></div>
          <div className="hint">{file ? `${(file.size / 1024 / 1024).toFixed(1)} MB von maximal ${maxMb} MB` : `.pptx mit Tonspur je Folie, maximal ${maxMb} MB`}</div>
        </label>

        <div className="row" style={{ marginTop: 16, justifyContent: "space-between" }}>
          <div className="field">
            <label htmlFor="lang">Feedbacksprache</label>
            <select id="lang" value={lang} onChange={(e) => setLang(e.target.value as Lang)} disabled={!!running}>
              <option value="auto">Automatisch</option>
              <option value="de">Deutsch</option>
              <option value="en">English</option>
            </select>
            <Help text={HELP.language} />
          </div>
          <div className="row">
            {file && !running && <button className="btn secondary" onClick={() => { setFile(null); setJob(null); setError(null); if (inputRef.current) inputRef.current.value = ""; }}>Zurücksetzen</button>}
            <button className="btn" onClick={submit} disabled={!file || busy || !!running}>
              {busy ? "Wird hochgeladen…" : "Bewerten"}
            </button>
            <Help text={HELP.grade} />
          </div>
        </div>
        {error && <p className="err" style={{ marginBottom: 0 }}>{error}</p>}
      </section>

      <section className="card">
        <h2>2. Aufgabe anpassen (optional) <Help text={HELP.context} /></h2>
        {config ? (
          <p className="small" style={{ marginTop: 0 }}>
            Aktuell ausgerichtet auf: <strong>{config.defaults.rubric.title}</strong> (Rubrik {config.defaults.rubric.version}, {config.defaults.rubric.max_points} Punkte,
            Kriterien: {config.defaults.rubric.criteria.join(", ")}). Aufgabenstellung: {config.defaults.task.first_line.replace(/^#+\s*/, "")}.
          </p>
        ) : <p className="small" style={{ marginTop: 0 }}>Standardkonfiguration wird geladen…</p>}
        <div className="row" style={{ gap: 20 }}>
          {(["rubric", "task", "case"] as const).map((k) => (
            <div className="field" key={k} style={{ flexDirection: "column", alignItems: "flex-start", gap: 4 }}>
              <label htmlFor={`ov-${k}`} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                {k === "rubric" ? "Rubrik" : k === "task" ? "Aufgabenstellung" : "Case-Text"} <Help text={HELP[k]} />
              </label>
              <input id={`ov-${k}`} ref={ovRefs[k]} type="file" disabled={!!running}
                accept={config ? config.accepted[k].join(",") : undefined}
                onChange={(e) => setOv((o) => ({ ...o, [k]: e.target.files?.[0] ?? null }))} />
            </div>
          ))}
        </div>
        {(ov.rubric || ov.task || ov.case) && (
          <p className="small">
            Für diesen Durchlauf: {[ov.rubric && `Rubrik ${ov.rubric.name}`, ov.task && `Aufgabe ${ov.task.name}`, ov.case && `Case ${ov.case.name}`].filter(Boolean).join(", ")}.{" "}
            <button className="btn secondary" style={{ padding: "4px 10px" }} onClick={() => { setOv({}); Object.values(ovRefs).forEach((r) => { if (r.current) r.current.value = ""; }); }}>Standard verwenden</button>
          </p>
        )}
      </section>

      {job && (
        <section className="card">
          <h2>3. Bewertung <Help text={HELP.result} /></h2>
          {running && (
            <div className="status">
              <span className="spinner" />
              <span>{STAGES[job.stage] ?? STAGES[job.status]}</span>
            </div>
          )}
          {job.status === "error" && <p className="err">Fehler: {job.error}</p>}
          {res && job.downloads && (
            <>
              <div className="row" style={{ justifyContent: "space-between" }}>
                <div>
                  <div className="small">{job.filename}</div>
                  <div className="score">{res.total_points} / {res.max_points} Punkte</div>
                </div>
                <div className="row">
                  <a className="btn" href={`${API}${job.downloads.docx}`}>Bewertung herunterladen (.docx)</a>
                  <a className="btn secondary" href={`${API}${job.downloads.md}`}>Markdown</a>
                  <a className="btn secondary" href={`${API}${job.downloads.json}`}>JSON</a>
                  <Help text={HELP.download} />
                </div>
              </div>
              {job.context && <p className="small">Bewertet mit: Rubrik {job.context.rubric.source}, Aufgabe {job.context.task.source}, Case {job.context.case.source}.</p>}
              <p className="small">Empfehlung der Gruppe: {res.recommendation_identified}</p>
              <p>{res.summary}</p>
              <table>
                <thead><tr><th>Kriterium</th><th>Niveau</th><th>Punkte</th></tr></thead>
                <tbody>
                  {res.criteria.map((c) => (
                    <tr key={c.id}><td>{c.name}</td><td>{LEVEL_LABEL[c.level]}</td><td>{c.points} / {c.max_points}</td></tr>
                  ))}
                </tbody>
              </table>
              {res.criteria.map((c) => (
                <details key={c.id}>
                  <summary>{c.name}</summary>
                  <p><strong>Was trägt.</strong> {c.was_traegt}</p>
                  <p><strong>Was bleibt dünn.</strong> {c.was_bleibt_duenn}</p>
                  <p><strong>Nächster Schritt.</strong> {c.naechster_schritt}</p>
                  {c.evidence.length > 0 && <><div className="small">Belege</div><ul>{c.evidence.map((e, i) => <li key={i}>{e}</li>)}</ul></>}
                </details>
              ))}
              <details>
                <summary>Abdeckung der Aufgaben <Help text={HELP.coverage} /></summary>
                <table>
                  <tbody>
                    {res.coverage.map((c) => (
                      <tr key={c.id}><td>{c.label}</td><td>{c.status}</td><td className="small">{c.note}</td></tr>
                    ))}
                  </tbody>
                </table>
              </details>
              <details>
                <summary>Vortrag (Tonspur) <Help text={HELP.delivery} /></summary>
                <ul>{res.delivery.map((d) => <li key={d.id}><strong>{d.label}.</strong> {d.observation}</li>)}</ul>
              </details>
              <details>
                <summary>Formale Checks <Help text={HELP.formal} /></summary>
                <ul>{checks.map((c) => <li key={c.id}>{c.ok === true ? "✓" : c.ok === false ? "✗" : "–"} {c.label}: {c.detail}</li>)}</ul>
              </details>
              {res.flags.length > 0 && (
                <details><summary>Manuell prüfen</summary><ul>{res.flags.map((f, i) => <li key={i}>{f}</li>)}</ul></details>
              )}
            </>
          )}
        </section>
      )}
    </main>
  );
}
