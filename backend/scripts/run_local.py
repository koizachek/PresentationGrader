"""Grade one PPTX from the command line.

    cd backend && uv run python scripts/run_local.py "../input/submission/Hoffmann Christoph.pptx" ../output/hoffmann
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.pipeline import run  # noqa: E402


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: run_local.py <file.pptx> [out_dir] [auto|de|en]")
    src = Path(sys.argv[1]).resolve()
    out = Path(sys.argv[2] if len(sys.argv) > 2 else f"../output/{src.stem}").resolve()
    lang = sys.argv[3] if len(sys.argv) > 3 else "auto"
    res = run(src, out, lang, lambda s, m: print(f"[{s}] {m}", flush=True))
    print(res["markdown"])
    print(f"\nDateien in {out}")


if __name__ == "__main__":
    main()
