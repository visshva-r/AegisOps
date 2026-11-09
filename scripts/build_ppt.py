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

# Safe layout band (inches): content must end above 6.15
FOOTER_LINE_Y = 6.82
FOOTER_TEXT_Y = 6.87
IMAGE_TOP = 1.72
IMAGE_MAX_H = 4.28
CAPTION_Y = 6.05
BODY_TOP = 1.72
BODY_TOP_SUB = 2.22


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
        MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(FOOTER_LINE_Y), Inches(12.3), Inches(0.02)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    line.line.fill.background()
    left = slide.shapes.add_textbox(Inches(0.55), Inches(FOOTER_TEXT_Y), Inches(7), Inches(0.3))
    lp = left.text_frame.paragraphs[0]
    lp.text = "AegisOps · DataOps Innovation Hackathon 2026 · PS-1"
    lp.font.size = Pt(9)
    lp.font.color.rgb = MUTED
    right = slide.shapes.add_textbox(Inches(10.3), Inches(FOOTER_TEXT_Y), Inches(2.5), Inches(0.3))
    rp = right.text_frame.paragraphs[0]
    rp.text = f"Slide {index}/{TOTAL_SLIDES}"
    rp.font.size = Pt(9)
    rp.font.color.rgb = MUTED
    rp.alignment = PP_ALIGN.RIGHT


def _heading(slide, title: str, subtitle: str | None = None, dark: bool = False) -> float:
    """Return Y (inches) where body content should start."""
    color = WHITE if dark else NAVY
    sub_color = SKY if dark else MUTED
    tx = slide.shapes.add_textbox(Inches(0.65), Inches(0.48), Inches(12.2), Inches(0.72))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = color
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.65), Inches(1.22), Inches(12.2), Inches(0.68))
        stf = st.text_frame
        stf.word_wrap = True
        sp = stf.paragraphs[0]
        sp.text = subtitle
        sp.font.size = Pt(13)
        sp.font.color.rgb = sub_color
        return BODY_TOP_SUB
    return BODY_TOP


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
    tx = slide.shapes.add_textbox(Inches(0.65), Inches(CAPTION_Y), Inches(12), Inches(0.45))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(10)
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
    slide.shapes.add_picture(str(path), Inches(left), Inches(top_in), width=Inches(w))


def _image_slide(slide, title: str, path: Path, caption: str, index: int) -> None:
    _set_bg(slide, LIGHT_BG)
    _bar(slide)
    _heading(slide, title)
    _footer(slide, index)
    _fit_image(slide, path, 0.75, IMAGE_TOP, 11.85, IMAGE_MAX_H)
    _caption(slide, caption)


def _content_slide(
    slide, title: str, items: list[str], index: int, subtitle: str | None = None
) -> None:
    _set_bg(slide, LIGHT_BG)
    _bar(slide)
    top = _heading(slide, title, subtitle)
    _footer(slide, index)
    _bullets(slide, items, top=top)


def _arch_flow_banner(slide, top: float = BODY_TOP) -> None:
    """Single-line pipeline (no overlapping shapes)."""
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.65),
        Inches(top),
        Inches(12.05),
        Inches(0.72),
    )
    box.fill.solid()
    box.fill.fore_color.rgb = BOX_FILL
    box.line.color.rgb = ACCENT
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Request  →  Scope  →  Plan  →  Scan  →  Correlate  →  Approve  →  PDF"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE


def main() -> None:
    prs = Presentation()
    prs.slide_width = int(SLIDE_W)
    prs.slide_height = int(SLIDE_H)
    blank = prs.slide_layouts[6]

    # Slide 1 — Cover
    s = prs.slides.add_slide(blank)
    _set_bg(s, NAVY)
    _bar(s, Inches(0.1))
    title = s.shapes.add_textbox(Inches(0.85), Inches(0.55), Inches(11.5), Inches(0.75))
    title.text_frame.paragraphs[0].text = "AegisOps"
    title.text_frame.paragraphs[0].font.size = Pt(40)
    title.text_frame.paragraphs[0].font.bold = True
    title.text_frame.paragraphs[0].font.color.rgb = WHITE
    sub = s.shapes.add_textbox(Inches(0.85), Inches(1.3), Inches(11.5), Inches(0.45))
    sub.text_frame.paragraphs[0].text = "Unified AI VAPT Agent · Problem Statement 1"
    sub.text_frame.paragraphs[0].font.size = Pt(16)
    sub.text_frame.paragraphs[0].font.color.rgb = SKY
    meta = s.shapes.add_textbox(Inches(0.85), Inches(2.05), Inches(11.5), Inches(1.35))
    mtf = meta.text_frame
    mtf.word_wrap = True
    for i, (line, color, size) in enumerate(
        [
            ("Participant: Visshva R (solo)", WHITE, 20),
            ("Event: DataOps Innovation Hackathon 2026", WHITE, 18),
            ("GitHub: github.com/visshva-r/AegisOps", SKY, 18),
        ]
    ):
        p = mtf.paragraphs[0] if i == 0 else mtf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.space_after = Pt(10)
    mission = s.shapes.add_textbox(Inches(0.85), Inches(3.55), Inches(10.8), Inches(1.75))
    misf = mission.text_frame
    misf.word_wrap = True
    mp = misf.paragraphs[0]
    mp.text = (
        "Mission: Turn analyst intent into correlated, auditable VAPT results "
        "with lab-only scope control and mandatory human approval."
    )
    mp.font.size = Pt(17)
    mp.font.color.rgb = SKY
    mp.line_spacing = 1.25
    _footer(s, 1)

    # Slide 2 — Team & PS (split)
    s = prs.slides.add_slide(blank)
    _set_bg(s, LIGHT_BG)
    _bar(s)
    body_top = _heading(
        s,
        "1. Team Introduction & Problem Statement",
        "Dashboard: Live / Import / Planned matrix",
    )
    _footer(s, 2)
    _bullets(
        s,
        [
            "Solo builder: Visshva R",
            "Challenge: PS-1 AI Unified VAPT Agent",
            "Product: conversational orchestration + audit trail",
            "Principle: augment analysts, never bypass scope or approval",
        ],
        width=5.1,
        top=body_top,
        size=16,
        height=4.2,
    )
    _fit_image(s, EVIDENCE / "shot1_home_recent.png", 5.95, body_top, 6.75, IMAGE_MAX_H)

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
    arch_top = _heading(s, "4. Project Architecture & Structure")
    _footer(s, 5)
    _arch_flow_banner(s, top=arch_top)
    _bullets(
        s,
        [
            "FastAPI UI and SQLite state for runs, tools, findings, audit",
            "Adapters: Nmap (live or fixture), Nikto and ZAP (import)",
            "Correlation engine: dedupe, confidence, risk order",
            "ReportLab generates the client VAPT PDF",
        ],
        top=arch_top + 1.0,
        size=17,
        height=4.0,
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
    box = s.shapes.add_textbox(Inches(1.25), Inches(3.35), Inches(10.8), Inches(2.35))
    tf = box.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Questions welcome."
    p1.font.size = Pt(28)
    p1.font.color.rgb = WHITE
    p1.alignment = PP_ALIGN.CENTER
    p1.space_after = Pt(42)
    p1.line_spacing = 1.0
    p2 = tf.add_paragraph()
    p2.text = "AegisOps keeps the analyst in control:"
    p2.font.size = Pt(21)
    p2.font.color.rgb = SKY
    p2.alignment = PP_ALIGN.CENTER
    p2.space_after = Pt(18)
    p2.line_spacing = 1.15
    p3 = tf.add_paragraph()
    p3.text = "scope · evidence · approval · report"
    p3.font.size = Pt(22)
    p3.font.color.rgb = WHITE
    p3.alignment = PP_ALIGN.CENTER
    _footer(s, 14)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
