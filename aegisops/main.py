from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from aegisops import __version__
from aegisops.agent.planner import build_plan
from aegisops.config import INTEGRATION_MATRIX
from aegisops.database import (
    audit,
    create_run,
    load_run,
    save_plan,
    update_status,
)
from aegisops.models import ApprovalRequest, AssessmentRequest, RunStatus
from aegisops.pipeline.orchestrator import execute_plan, prepare_validation_queue
from aegisops.report.pdf import build_vapt_pdf
from aegisops.scope import ScopeError, validate_scope

BASE = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE / "templates"))

app = FastAPI(title="AegisOps", version=__version__, description="Unified VAPT AI Agent")
app.mount("/static", StaticFiles(directory=str(BASE / "static")), name="static")


def _run_banner(run: dict) -> tuple[str, str] | None:
    status = run["status"]
    audit = run.get("audit") or []
    if status == RunStatus.REJECTED:
        return ("error", "Validation rejected by analyst.")
    if status == RunStatus.COMPLETE:
        if any(a.get("action") == "approval_granted" for a in audit):
            return (
                "ok",
                "Assessment completed · Human validation approval logged to audit trail.",
            )
        return ("ok", "Assessment complete · No active validation was required.")
    if status == RunStatus.AWAITING_APPROVAL:
        return (
            "warn",
            "High-severity findings detected · approve validation to finalize the audit trail before client delivery.",
        )
    return None


def _run_context(run: dict, **extra) -> dict:
    ctx = {"run": run, "banner": _run_banner(run), **extra}
    return ctx


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    from aegisops.database import list_recent_runs

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "version": __version__,
            "matrix": INTEGRATION_MATRIX,
            "recent_runs": list_recent_runs(),
        },
    )


@app.post("/assessments", response_class=HTMLResponse)
def start_assessment(
    request: Request,
    analyst_request: str = Form(...),
    target: str = Form(...),
    exclusions: str = Form(""),
):
    try:
        normalized, scope_msg = validate_scope(target, exclusions)
    except ScopeError as exc:
        from aegisops.database import list_recent_runs

        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "error": str(exc),
                "version": __version__,
                "matrix": INTEGRATION_MATRIX,
                "recent_runs": list_recent_runs(),
            },
            status_code=400,
        )

    req = AssessmentRequest(
        analyst_request=analyst_request, target=normalized, exclusions=exclusions
    )
    run_id = create_run(req)
    audit(run_id, "scope_validated", scope_msg)
    plan = build_plan(req, normalized)
    save_plan(run_id, plan)
    return templates.TemplateResponse(
        request,
        "run.html",
        _run_context(load_run(run_id), scope_msg=scope_msg),
    )


@app.post("/assessments/{run_id}/execute", response_class=HTMLResponse)
def run_scans(request: Request, run_id: str):
    run = load_run(run_id)
    if not run or not run["plan"]:
        raise HTTPException(404, "Run or plan not found")
    execute_plan(run_id, run["plan"], run["target"])
    run = load_run(run_id)
    pending = prepare_validation_queue(run["findings"])
    if pending:
        update_status(run_id, RunStatus.AWAITING_APPROVAL)
        audit(run_id, "awaiting_approval", f"{len(pending)} validation action(s)")
    else:
        update_status(run_id, RunStatus.COMPLETE)
    return templates.TemplateResponse(
        request,
        "run.html",
        _run_context(load_run(run_id), pending_validation=pending),
    )


@app.post("/assessments/{run_id}/approve", response_class=HTMLResponse)
def approve_validation(
    request: Request,
    run_id: str,
    approved: str = Form(...),
    note: str = Form(""),
):
    body = ApprovalRequest(approved=approved.lower() == "true", note=note)
    if body.approved:
        audit(run_id, "approval_granted", body.note or "Analyst approved lab validation")
        update_status(run_id, RunStatus.APPROVED)
        audit(run_id, "metasploit_stub", "Import-only Metasploit validation recorded (no autonomous exploit)")
        update_status(run_id, RunStatus.COMPLETE)
    else:
        audit(run_id, "approval_denied", body.note or "Analyst rejected active validation")
        update_status(run_id, RunStatus.REJECTED)
    return templates.TemplateResponse(
        request,
        "run.html",
        _run_context(load_run(run_id), pending_validation=[]),
    )


@app.get("/assessments/{run_id}", response_class=HTMLResponse)
def view_run(request: Request, run_id: str):
    run = load_run(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    pending = []
    if run["status"] == RunStatus.AWAITING_APPROVAL:
        pending = prepare_validation_queue(run["findings"])
    return templates.TemplateResponse(
        request,
        "run.html",
        _run_context(run, pending_validation=pending),
    )


@app.get("/assessments/{run_id}/report.pdf")
def download_report(run_id: str):
    run = load_run(run_id)
    if not run:
        raise HTTPException(404, "Run not found")
    pdf = build_vapt_pdf(
        run_id,
        run["target"],
        run["analyst_request"],
        run["findings"],
        run["tool_runs"],
        run["audit"],
    )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="aegisops-vapt-{run_id[:8]}.pdf"'},
    )


@app.get("/api/integration-matrix")
def integration_matrix():
    return {"integrations": INTEGRATION_MATRIX}
