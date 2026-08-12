"""Extract embedded figures from the committed notebook outputs.

Uses only the standard library. The notebooks are committed with their
outputs, so the PNGs written here are the exact figures produced by the
saved runs, not regenerated approximations.

Run with: python scripts/extract_figures.py
"""

import base64
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "docs" / "images"

# (notebook filename, cell title fragment to match, output filename)
FIGURES = [
    (
        "Exploratory Data Analysis.ipynb",
        "Share of Students by Outcome",
        "outcome-distribution.png",
    ),
    (
        "Capstone File.ipynb",
        "ROC Curves (test set)",
        "roc-curves.png",
    ),
]


def extract(notebook: Path, title_fragment: str, destination: Path) -> None:
    cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
    for cell in cells:
        source = "".join(cell.get("source", []))
        if title_fragment not in source:
            continue
        for output in cell.get("outputs", []):
            png_b64 = output.get("data", {}).get("image/png")
            if png_b64:
                destination.write_bytes(base64.b64decode(png_b64))
                print(f"Wrote {destination} ({destination.stat().st_size} bytes)")
                return
    raise SystemExit(
        f"No PNG output found for a cell containing {title_fragment!r} in {notebook.name}"
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for notebook_name, title_fragment, output_name in FIGURES:
        extract(REPO_ROOT / notebook_name, title_fragment, OUTPUT_DIR / output_name)


if __name__ == "__main__":
    main()
