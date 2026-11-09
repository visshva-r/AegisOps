from __future__ import annotations

import io
from collections import Counter
from datetime import datetime, timezone

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from aegisops.models import UnifiedFinding


def build_vapt_pdf(
    run_id: str,
    target: str,
    analyst_request: str,
    findings: list[UnifiedFinding],
    tool_runs: list[dict],
    audit: list[dict],
) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=2 * cm, leftMargin=2 * cm)
    styles = getSampleStyleSheet()
    h1 = styles["Heading1"]
    h2 = styles["Heading2"]
    body = ParagraphStyle("Body", parent=styles["Normal"], spaceAfter=8)

    sev_counts = Counter(f.severity for f in findings)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    story = [
        Paragraph("Vulnerability Assessment & Penetration Test Report", h1),
        Paragraph(f"<b>Assessment ID:</b> {run_id}", body),
        Paragraph(f"<b>Target:</b> {target}", body),
        Paragraph(f"<b>Generated:</b> {now}", body),
        Spacer(1, 12),
        Paragraph("1. Executive Summary", h2),
        Paragraph(
            f"This authorized lab assessment addressed: {analyst_request}. "
            f"The agent orchestrated {len(tool_runs)} tool executions/imports, "
            f"correlated {len(findings)} unified findings with evidence traceability.",
            body,
        ),
        Paragraph("2. Assessment Methodology", h2),
        Paragraph(
            "Workflow: scope validation → adaptive planning → approved scan orchestration → "
            "ingestion → AI correlation → risk prioritization → human approval → reporting. "
            "References: NIST SP 800-115, OWASP Top 10, CVSS concepts.",
            body,
        ),
        Paragraph("3. Severity Distribution", h2),
    ]

    dist_data = [["Severity", "Count"]] + [[k, str(v)] for k, v in sorted(sev_counts.items())]
    dist_table = Table(dist_data, colWidths=[6 * cm, 3 * cm])
    dist_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ]
        )
    )
    story.append(dist_table)
    story.append(Spacer(1, 12))
    story.append(Paragraph("4. Detailed Findings", h2))

    for i, f in enumerate(findings[:25], 1):
        story.append(Paragraph(f"<b>{i}. {f.title}</b> [{f.severity.upper()}]", body))
        story.append(
            Paragraph(
                f"Assets: {', '.join(f.assets)} | Sources: {', '.join(f.sources)} | "
                f"Confidence: {f.confidence} | Status: {f.validation_status} | Kind: {f.kind.value}",
                body,
            )
        )
        story.append(Paragraph(f.description, body))
        if f.cve:
            story.append(Paragraph(f"<b>Reference:</b> {f.cve}", body))
        story.append(
            Paragraph(
                f"<b>Evidence:</b> {'; '.join(f.evidence_refs[:3])}",
                body,
            )
        )
        story.append(Paragraph(f"<b>Remediation:</b> {f.remediation}", body))
        story.append(Spacer(1, 6))

    story.append(Paragraph("5. Tool Execution Summary", h2))
    tool_rows = [["Tool", "Mode", "Status", "Output"]]
    for tr in tool_runs:
        tool_rows.append(
            [tr.get("tool", ""), tr.get("mode", ""), tr.get("status", ""), tr.get("output_ref", "")[:60]]
        )
    tt = Table(tool_rows, colWidths=[3 * cm, 2.5 * cm, 4 * cm, 6 * cm])
    tt.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.25, colors.grey)]))
    story.append(tt)

    story.append(Spacer(1, 12))
    story.append(Paragraph("6. Limitations & Approvals", h2))
    story.append(
        Paragraph(
            "Testing limited to organizer-authorized lab targets. Active exploitation requires "
            "explicit human approval (audit trail retained). LLM/agent conclusions are grounded "
            "in tool outputs; inferred items are labeled.",
            body,
        )
    )
    approval_lines = [a for a in audit if "approval" in a.get("action", "")]
    if approval_lines:
        story.append(Paragraph("<b>Human approval events:</b>", body))
        for a in approval_lines[-5:]:
            story.append(Paragraph(f"{a.get('created_at')}: {a.get('detail')}", body))

    doc.build(story)
    return buf.getvalue()
