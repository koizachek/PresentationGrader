from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # reads backend/.env and the repo-root .env (root wins)
    model_config = SettingsConfigDict(env_file=(".env", "../.env"), extra="ignore")

    # --- Mistral (grading + transcription) ---
    mistral_api_key: str = ""
    mistral_server: str = "global"  # global (api.mistral.ai) | eu | us
    mistral_model: str = "mistral-large-latest"
    mistral_transcribe_model: str = "voxtral-mini-latest"
    transcribe_language: str = ""  # "" = auto-detect, else e.g. "de"
    # notes = no speech-to-text, speaker notes stand in (dev only)
    transcriber: str = "mistral"  # mistral | notes

    # --- feedback ---
    feedback_language: str = "auto"  # auto | de | en

    # --- server ---
    frontend_origin: str = "http://localhost:3000"
    max_upload_mb: int = 200
    render_slides: bool = True
    # Nothing is written to disk beyond a temp dir that is deleted after grading.
    # Finished reports stay in memory for this many hours for download (0 = until restart).
    report_retention_hours: float = 1

    # --- grading context (swap these to reuse the app for another case) ---
    rubric_path: Path = Path(__file__).parent / "rubrics" / "meditec_pitch.yaml"
    case_path: Path = Path(__file__).parent / "rubrics" / "case_meditec.md"
    task_path: Path = Path(__file__).parent / "rubrics" / "task.md"


settings = Settings()
