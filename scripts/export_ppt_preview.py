"""Export each PPTX slide to PNG via PowerPoint COM (Windows)."""
from __future__ import annotations

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PPTX = BASE / "ppt" / "AegisOps_DataOps_Hackathon_2026.pptx"
OUT = BASE / "ppt" / "preview"


def main() -> int:
    if not PPTX.is_file():
        print(f"Missing {PPTX}", file=sys.stderr)
        return 1
    try:
        import win32com.client  # type: ignore
    except ImportError:
        print("Install pywin32: pip install pywin32", file=sys.stderr)
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    app = win32com.client.Dispatch("PowerPoint.Application")
    app.Visible = 1
    pres = app.Presentations.Open(str(PPTX.resolve()), WithWindow=False, ReadOnly=True)
    try:
        for i in range(1, pres.Slides.Count + 1):
            target = str(OUT / f"slide_{i:02d}.png")
            pres.Slides(i).Export(target, "PNG", 1920, 1080)
            print(target)
    finally:
        pres.Close()
        app.Quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
