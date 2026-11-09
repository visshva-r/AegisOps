"""Generate Unstop submission PPTX from SLIDE_CONTENT + evidence screenshots."""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

BASE = Path(__file__).resolve().parent.parent
EVIDENCE = BASE / "evidence" / "demo"
OUT = BASE / "ppt" / "AegisOps_DataOps_Hackathon_2026.pptx"

ACCENT = RGBColor(0x0C, 0x4A, 0x6E)
TEXT = RGBColor(0x1E, 0x29, 0x3B)
MUTED = RGBColor(0x47, 0x55, 0x69)


def _title(slide, text: str, subtitle: str | None = None) -> None:
    tx = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12), Inches(0.9))
    p = tx.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = ACCENT
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.6), Inches(1.05), Inches(12), Inches(0.5))
        sp = st.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(14)
        sp.font.color.rgb = MUTED


def _bullets(slide, items: list[str], left=0.6, top=1.6, width=8.8, height=5.0) -> None:
    tx = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tx.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item
        p.level = 0
        p.font.size = Pt(18)
        p.font.color.rgb = TEXT
        p.space_after = Pt(8)


def _image(slide, path: Path, left, top, width) -> None:
    if path.is_file():
        slide.shapes.add_picture(str(path), Inches(left), Inches(top), width=Inches(width))


def main() -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # 1 Team Introduction & Problem Statement
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "AegisOps", "Team & Problem Statement — DataOps Innovation Hackathon 2026 | PS-1")
    _bullets(
        s,
        [
            "Solo participant · GitHub: github.com/visshva-r/AegisOps",
            "Problem Statement 1: AI Unified VAPT Agent",
            "Goal: NL analyst request → scoped orchestration → correlation → human approval → PDF",
            "Safety: lab targets only; no autonomous exploitation",
        ],
        top=1.35,
        width=6.2,
    )
    _image(s, EVIDENCE / "shot1_home_recent.png", 6.9, 1.2, 6.0)

    # 2 The Problem
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "The Problem")
    _bullets(
        s,
        [
            "Fragmented scanners (Nmap, Nikto, ZAP, Nessus) produce incompatible raw outputs",
            "Duplicate alerts with inconsistent severity; weak cross-tool correlation",
            "Risk of autonomous exploitation and out-of-scope targets",
            "Auditors need traceability from report findings to raw tool evidence",
        ],
    )

    # 3 Your Solution
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Your Solution — AegisOps")
    _bullets(
        s,
        [
            "Scope enforcement before any scan (reject e.g. 8.8.8.8)",
            "Adaptive plan with per-tool rationale (not a fixed script)",
            "Normalize, dedupe, correlate; confidence + observed vs inferred",
            "Human approval gate before active validation (Metasploit stub)",
            "Client-ready VAPT PDF with evidence references",
        ],
        width=6.2,
    )
    _image(s, EVIDENCE / "shot2_scope_rejection.png", 6.9, 1.3, 6.0)

    # 4 Architecture
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Architecture & Workflow")
    _bullets(
        s,
        [
            "Request → scope.py → planner.py → adapters → correlate.py",
            "SQLite: runs, tool_runs, findings, audit_log",
            "UI: FastAPI + Jinja2 · Report: ReportLab PDF",
            "Workflow: Plan → Orchestrate → Analyze → Approve → Report",
        ],
        width=6.0,
        height=3.2,
        top=1.4,
    )
    _image(s, EVIDENCE / "shot3_planned_plan.png", 6.7, 1.2, 6.2)

    # 5 Tech Stack
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Tech Stack")
    _bullets(
        s,
        [
            "Python 3.10+, FastAPI, Pydantic v2, SQLite",
            "Jinja2 templates + responsive CSS dashboard",
            "ReportLab for multi-page VAPT PDF",
            "Tool adapters: Nmap (live/fallback), Nikto + ZAP (import), Metasploit (approval stub)",
            "Honest integration matrix: Live / Import / Planned",
        ],
    )

    # 6 Features — Judge checklist
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Features (PS-1 Judge Checklist §10)")
    _bullets(
        s,
        [
            "1–2: NL request + scope validation; adaptive plan with rationale",
            "3–4: Multi-tool ingestion; dedupe + confidence + correlation labels",
            "5: Risk sort + mandatory human approval before validation",
            "6: Downloadable PDF traced to fixture evidence",
            "7: Transparent matrix; no false live scanner claims",
        ],
        width=6.0,
        height=4.5,
        top=1.35,
    )
    _image(s, EVIDENCE / "shot4_awaiting_approval.png", 6.65, 1.15, 6.25)

    # 6b Features continued with complete state
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Audit Trail & VAPT Report")
    _bullets(
        s,
        [
            "Immutable audit: scope, agent_decision, tool_complete, approval_granted",
            "4-page PDF: executive summary, methodology, findings, limitations",
            "Recent lab runs on home for demo continuity",
        ],
        width=6.0,
        top=1.4,
    )
    _image(s, EVIDENCE / "shot5_complete_audit_pdf.png", 6.65, 1.15, 6.25)

    # 7 Feasibility
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Feasibility")
    _bullets(
        s,
        [
            "Runs locally: venv + pip install + python run.py",
            "Fixture fallback when Nmap absent; demos stay reliable",
            "Sub-second orchestration on lab fixtures (validated in QA)",
            "Extendable: Docker/K8s, background workers for long scans",
        ],
    )

    # 8 Limitations
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Limitations")
    _bullets(
        s,
        [
            "Lab allowlist only; enterprise RBAC not implemented",
            "Long live scans need async job queue for production",
            "Metasploit: human-gated stub only (no autonomous exploit)",
            "Nessus/OpenVAS/Burp: planned or import — not claimed as live",
        ],
    )

    # 9 Future Scope
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Future Scope")
    _bullets(
        s,
        [
            "LLM planner for richer reasoning (extension point in planner.py)",
            "Nessus / OpenVAS / Burp enterprise connectors",
            "Attack-path visualization and remediation playbooks",
            "CI/CD security gate (GitHub Action / GitLab CI)",
        ],
    )
    # Closing slide
    s = prs.slides.add_slide(prs.slide_layouts[6])
    _title(s, "Thank You", "github.com/visshva-r/AegisOps · Questions?")
    box = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11), Inches(2))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = (
        "Intelligent VAPT orchestration with strict scope, honest tool transparency, "
        "and the human analyst in control of consequential actions."
    )
    p.font.size = Pt(22)
    p.font.color.rgb = TEXT
    p.alignment = PP_ALIGN.CENTER

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
