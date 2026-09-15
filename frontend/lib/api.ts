const DEFAULT_API = "https://presentationgrader-production.up.railway.app";
// Accept the raw Railway domain, with or without protocol, trailing slash or a stray /api suffix.
function normalize(raw: string | undefined): string {
  let u = (raw ?? "").trim();
  if (!u) return DEFAULT_API;
  if (!/^https?:\/\//i.test(u)) u = `https://${u}`;
  return u.replace(/\/+$/, "").replace(/\/api$/i, "");
}
export const API = normalize(process.env.NEXT_PUBLIC_API_URL);

export type Level = "ueberzeugend" | "tragfaehig" | "ansatzweise";
export const LEVEL_LABEL: Record<Level, string> = {
  ueberzeugend: "überzeugend", tragfaehig: "tragfähig", ansatzweise: "ansatzweise",
};

export type Criterion = {
  id: string; name: string; level: Level; points: number; max_points: number;
  was_traegt: string; was_bleibt_duenn: string; naechster_schritt: string; evidence: string[];
};
export type CoverageItem = { id: string; label: string; status: "adressiert" | "teilweise" | "fehlt"; note: string };
export type DeliveryNote = { id: string; label: string; observation: string };
export type FormalCheck = { id: string; label: string; ok: boolean | null; detail: string };

export type GradingResult = {
  total_points: number; max_points: number; recommendation_identified: string; summary: string;
  strengths: string[]; weaknesses: string[]; criteria: Criterion[];
  coverage: CoverageItem[]; delivery: DeliveryNote[];
  slide_notes: { slide: number; observation: string }[]; flags: string[];
};

export type Job = {
  id: string; filename: string; language: string; context: ContextSummary | null;
  status: "queued" | "running" | "done" | "error";
  stage: string; message: string; error: string | null;
  result: { result: GradingResult; formal_checks: FormalCheck[]; metrics: Record<string, unknown>; markdown: string } | null;
  downloads: { docx: string; md: string; json: string } | null;
};

export type Overrides = { rubric?: File | null; task?: File | null; case?: File | null };

export type ContextSummary = {
  rubric: { title: string; version: string; max_points: number | null; criteria: string[]; source: string };
  task: { words: number; first_line: string; source: string };
  case: { words: number; first_line: string; source: string };
};

export type Config = { defaults: ContextSummary; accepted: { rubric: string[]; task: string[]; case: string[] }; max_upload_mb: number };

export async function fetchConfig(): Promise<Config> {
  const r = await fetch(`${API}/api/config`, { cache: "no-store" });
  if (!r.ok) throw new Error(`Konfiguration konnte nicht geladen werden (${r.status})`);
  return r.json();
}

export async function uploadSubmission(file: File, language: "auto" | "de" | "en" = "auto", overrides: Overrides = {}): Promise<Job> {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("language", language);
  if (overrides.rubric) fd.append("rubric", overrides.rubric);
  if (overrides.task) fd.append("task", overrides.task);
  if (overrides.case) fd.append("case", overrides.case);
  const r = await fetch(`${API}/api/jobs`, { method: "POST", body: fd });
  if (!r.ok) throw new Error((await r.json().catch(() => ({})))?.detail ?? `Upload fehlgeschlagen (${r.status}) – Backend: ${API}`);
  return r.json();
}

export async function fetchJob(id: string): Promise<Job> {
  const r = await fetch(`${API}/api/jobs/${id}`, { cache: "no-store" });
  if (!r.ok) throw new Error(`Status konnte nicht geladen werden (${r.status})`);
  return r.json();
}
