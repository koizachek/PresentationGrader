export const API = (process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000").replace(/\/$/, "");

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
  id: string; filename: string; language: string;
  status: "queued" | "running" | "done" | "error";
  stage: string; message: string; error: string | null;
  result: { result: GradingResult; formal_checks: FormalCheck[]; metrics: Record<string, unknown>; markdown: string } | null;
  downloads: { docx: string; md: string; json: string } | null;
};

export async function uploadSubmission(file: File, language: "auto" | "de" | "en" = "auto"): Promise<Job> {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("language", language);
  const r = await fetch(`${API}/api/jobs`, { method: "POST", body: fd });
  if (!r.ok) throw new Error((await r.json().catch(() => ({})))?.detail ?? `Upload fehlgeschlagen (${r.status})`);
  return r.json();
}

export async function fetchJob(id: string): Promise<Job> {
  const r = await fetch(`${API}/api/jobs/${id}`, { cache: "no-store" });
  if (!r.ok) throw new Error(`Status konnte nicht geladen werden (${r.status})`);
  return r.json();
}
