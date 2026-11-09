"""Generate polished Unstop submission PPTX (9 mandatory sections + cover + close)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

BASE = Path(__file__).resolve().parent.parent
EVIDENCE = BASE / "evidence" / "demo"
OUT = BASE / "ppt" / "AegisOps_DataOps_Hackathon_2026.pptx"

NAVY = RGBColor(0x0F, 0x17, 0x2A)
ACCENT = RGBColor(0x03, 0x82, 0xF6)
SKY = RGBColor(0x38, 0xBD, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
TEXT = RGBColor(0x1E, 0x29, 0x3B)
MUTED = RGBColor(0x64, 0x74, 0x8B)
LIGHT_BG = RGBColor(0xF8, 0xFA, 0xFC)
BOX_FILL = RGBColor(0xE0, 0xF2, 0xFE)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
TOTAL_SLIDES = 14


def _set_bg(slide, color: RGBColor) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def _bar(slide, height=Inches(0.14)) -> None:
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, height)
    sh.fill.solid()
    sh.fill.fore_color.rgb = ACCENT
    sh.line.fill.background()


def _footer(slide, index: int) -> None:
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(6.88), Inches(12.3), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    line.line.fill.background()
    tx = slide.shapes.add_textbox(Inches(0.5), Inches(6.92), Inches(12.3), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = f"AegisOps  |  DataOps Innovation Hackathon 2026  |  PS-1     Slide {index}/{TOTAL_SLIDES}"
    p.font.size = Pt(10)
    p.font.color.rgb = MUTED
    p.alignment = PP_ALIGN.RIGHT


def _heading(slide, title: str, subtitle: str | None = None, dark: bool = False) -> None:
    color = WHITE if dark else NAVY
    sub_color = SKY if dark else MUTED
    tx = slide.shapes.add_textbox(Inches(0.65), Inches(0.42), Inches(12), Inches(0.8))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = color
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.65), Inches(1.05), Inches(12), Inches(0.5))
        sp = st.text_frame.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(14)
        sp.font.color.rgb = sub_color


def _bullets(
    slide,
    items: list[str],
    *,
    left=0.75,
    top=1.75,
    width=11.5,
    height=4.9,
    size=19,
    color=TEXT,
) -> None:
    tx = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = item if item.startswith("•") else f"•  {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(14)
        p.line_spacing = 1.15


def _caption(slide, text: str) -> None:
    tx = slide.shapes.add_textbox(Inches(0.65), Inches(6.55), Inches(12), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(11)
    p.font.italic = True
    p.font.color.rgb = MUTED
    p.alignment = PP_ALIGN.CENTER


def _fit_image(slide, path: Path, left_in: float, top_in: float, max_w_in: float, max_h_in: float) -> None:
    """Insert image scaled to fit box (avoids footer overlap)."""
    if not path.is_file():
        return
    with Image.open(path) as im:
        iw, ih = im.size
    aspect = ih / iw
    w = max_w_in
    h = w * aspect
    if h > max_h_in:
        h = max_h_in
        w = h / aspect
    left = left_in + (max_w_in - w) / 2
    pic = slide.shapes.add_picture(str(path), Inches(left), Inches(top_in), width=Inches(w))
    # subtle border
    frame = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left) - Inches(0.04),
        Inches(top_in) - Inches(0.04),
        Inches(w) + Inches(0.08),
        Inches(h) + Inches(0.08),
    )
    frame.fill.background()
    frame.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
    frame.line.width = Pt(1.5)
    # send border behind picture
    slide.shapes._spTree.remove(frame._element)
    slide.shapes._spTree.insert(2, frame._element)


def _image_slide(slide, title: str, path: Path, caption: str, index: int) -> None:
    _set_bg(slide, LIGHT_BG)
    _bar(slide)
    _heading(slide, title)
    _footer(slide, index)
    _fit_image(slide, path, 0.85, 1.45, 11.6, 4.85)
    _caption(slide, caption)


def _content_slide(
    slide, title: str, items: list[str], index: int, subtitle: str | None = None
) -> None:
    _set_bg(slide, LIGHT_BG)
    _bar(slide)
    _heading(slide, title, subtitle)
    _footer(slide, index)
    _bullets(slide, items)


def _arch_diagram(slide) -> None:
    """Simple horizontal pipeline diagram."""
    steps = [
        "Scope",
        "Plan",
        "Scan",
        "Correlate",
        "Approve",
        "PDF",
    ]
    x0 = 0.7
    y = 2.05
    w = 1.75
    h = 0.65
    gap = 0.28
    for i, label in enumerate(steps):
        left = x0 + i * (w + gap)
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(y), Inches(w), Inches(h)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = BOX_FILL
        box.line.color.rgb = ACCENT
        tf = box.text_frame
        tf.paragraphs[0].text = label
        tf.paragraphs[0].font.size = Pt(13)
        tf.paragraphs[0].font.bold = True
        tf.paragraphs[0].font.color.rgb = NAVY
        tf.paragraphs[0].alignment = PP_ALIGN.CENTER
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        if i < len(steps) - 1:
            arr = slide.shapes.add_textbox(
                Inches(left + w + 0.05), Inches(y + 0.15), Inches(gap), Inches(0.4)
            )
            arr.text_frame.paragraphs[0].text = "→"
            arr.text_frame.paragraphs[0].font.size = Pt(18)
            arr.text_frame.paragraphs[0].font.color.rgb = ACCENT


def main() -> None:
    prs = Presentation()
    prs.slide_width = int(SLIDE_W)
    prs.slide_height = int(SLIDE_H)
    blank = prs.slide_layouts[6]

    # Slide 1 — Cover
    s = prs.slides.add_slide(blank)
    _set_bg(s, NAVY)
    _bar(s, Inches(0.1))
    _heading(s, "AegisOps", "Unified AI VAPT Agent  ·  Problem Statement 1", dark=True)
    team = s.shapes.add_textbox(Inches(0.85), Inches(2.1), Inches(11.5), Inches(3.8))
    tf = team.text_frame
    lines = [
        ("Participant: Visshva R (solo)", WHITE, 21),
        ("Event: DataOps Innovation Hackathon 2026", WHITE, 19),
        ("GitHub: github.com/visshva-r/AegisOps", SKY, 19),
        ("", WHITE, 10),
        (
            "Mission: Turn analyst intent into correlated, auditable VAPT results "
            "with lab-only scope control and mandatory human approval.",
            SKY,
            18,
        ),
    ]
    for i, (line, color, size) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(12)
    _footer(s, 1)

    # Slide 2 — Team & PS (split)
    s = prs.slides.add_slide(blank)
    _set_bg(s, LIGHT_BG)
    _bar(s)
    _heading(s, "1. Team Introduction & Problem Statement")
    _footer(s, 2)
    _bullets(
        s,
        [
            "Solo builder: Visshva R",
            "Challenge: PS-1 AI Unified VAPT Agent",
            "Product: conversational orchestration + audit trail",
            "Principle: augment analysts, never bypass scope or approval",
        ],
        width=5.4,
        top=1.7,
        size=17,
    )
    _fit_image(
        s,
        EVIDENCE / "shot1_home_recent.png",
        6.35,
        1.55,
        6.55,
        4.75,
    )
    _caption(s, "Live/Import/Planned matrix and recent lab runs.")

    # Slide 3 — Problem
    s = prs.slides.add_slide(blank)
    _content_slide(
        s,
        "2. The Problem",
        [
            "Many scanners, many formats (XML, JSON, text)",
            "Duplicate alerts and mismatched severity waste analyst time",
            "Autonomous pentest bots can hit out-of-scope assets",
            "Executives need findings linked to verifiable raw evidence",
        ],
        3,
    )

    # Slide 4 — Solution + screenshot
    s = prs.slides.add_slide(blank)
    _image_slide(
        s,
        "3. Your Solution",
        EVIDENCE / "shot2_scope_rejection.png",
        "Out-of-scope targets are rejected before any scan is queued.",
        4,
    )

    # Slide 5 — Architecture text + diagram
    s = prs.slides.add_slide(blank)
    _set_bg(s, LIGHT_BG)
    _bar(s)
    _heading(s, "4. Project Architecture & Structure")
    _footer(s, 5)
    _arch_diagram(s)
    _bullets(
        s,
        [
            "FastAPI UI and SQLite state for runs, tools, findings, audit",
            "Adapters: Nmap (live or fixture), Nikto and ZAP (import)",
            "Correlation engine: dedupe, confidence, risk order",
            "ReportLab generates the client VAPT PDF",
        ],
        top=3.05,
        size=17,
    )

    # Slide 6 — Architecture screenshot
    s = prs.slides.add_slide(blank)
    _image_slide(
        s,
        "4. Architecture (Live Workflow)",
        EVIDENCE / "shot3_planned_plan.png",
        "Adaptive plan with explicit rationale for each tool stage.",
        6,
    )

    # Slide 7 — Tech stack
    s = prs.slides.add_slide(blank)
    _content_slide(
        s,
        "5. Tech Stack",
        [
            "Python 3.10+, FastAPI, Pydantic v2, SQLite",
            "Jinja2 templates and responsive CSS dashboard",
            "ReportLab PDF (executive + technical sections)",
            "Nmap, Nikto, OWASP ZAP integrations; Metasploit approval stub",
        ],
        7,
    )

    # Slide 8 — Features list
    s = prs.slides.add_slide(blank)
    _content_slide(
        s,
        "6. Features (Judge Checklist §10)",
        [
            "NL request and lab scope validation",
            "Adaptive plan with tool rationale",
            "Multi-tool ingest with traceable output paths",
            "Correlation, dedupe, confidence, observed vs inferred",
            "Human approval before active validation",
            "VAPT PDF download and honest integration matrix",
        ],
        8,
        subtitle="All seven PS-1 demonstration items implemented",
    )

    # Slides 9–10 — Feature screenshots
    s = prs.slides.add_slide(blank)
    _image_slide(
        s,
        "6. Features — Approval Gate",
        EVIDENCE / "shot4_awaiting_approval.png",
        "Execution pauses until the analyst approves validation.",
        9,
    )

    s = prs.slides.add_slide(blank)
    _image_slide(
        s,
        "6. Features — Audit & Report",
        EVIDENCE / "shot5_complete_audit_pdf.png",
        "Audit trail and one-click VAPT PDF export.",
        10,
    )

    # Slide 11–13 — Feasibility, limitations, future
    s = prs.slides.add_slide(blank)
    _content_slide(
        s,
        "7. Feasibility",
        [
            "Runs locally: pip install and python run.py",
            "Fixtures keep demos stable without commercial licenses",
            "Transparent Live / Import / Planned labels in UI and API",
            "Ready to extend with workers, Docker, and enterprise APIs",
        ],
        11,
    )

    s = prs.slides.add_slide(blank)
    _content_slide(
        s,
        "8. Limitations",
        [
            "Lab allowlist only (no multi-tenant RBAC yet)",
            "Long live scans need background jobs at scale",
            "No autonomous exploitation; Metasploit stub after approval",
            "Nessus, OpenVAS, Burp not live in this prototype",
        ],
        12,
    )

    s = prs.slides.add_slide(blank)
    _content_slide(
        s,
        "9. Future Scope",
        [
            "LLM planner and remediation narratives",
            "Nessus, OpenVAS, and Burp enterprise connectors",
            "Attack-path visualization and SIEM export",
            "CI/CD security gate for release pipelines",
        ],
        13,
    )

    # Slide 14 — Thank you
    s = prs.slides.add_slide(blank)
    _set_bg(s, NAVY)
    _heading(s, "Thank You", "github.com/visshva-r/AegisOps", dark=True)
    box = s.shapes.add_textbox(Inches(1.0), Inches(2.75), Inches(11.3), Inches(2.0))
    p = box.text_frame.paragraphs[0]
    p.text = (
        "Questions welcome.\n\n"
        "AegisOps keeps the analyst in control:\n"
        "scope, evidence, approval, and report."
    )
    p.font.size = Pt(26)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    _footer(s, 14)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
