from __future__ import annotations

from aegisops.adapters import ADAPTERS, run_adapter
from aegisops.agent.planner import next_step_rationale
from aegisops.database import add_tool_run, audit, save_findings, update_status
from aegisops.models import RawFinding, RunStatus, UnifiedFinding
from aegisops.pipeline.correlate import correlate_and_dedupe


def execute_plan(run_id: str, plan, target: str) -> tuple[list[UnifiedFinding], list[str]]:
    raw_findings: list[RawFinding] = []
    rationales: list[str] = []
    completed: list[str] = []

    update_status(run_id, RunStatus.SCANNING)

    for step in sorted(plan.steps, key=lambda s: s.order):
        adapter = ADAPTERS.get(step.tool)
        if not adapter:
            audit(run_id, "tool_skipped", f"Unsupported: {step.tool}")
            continue
        use_live = step.mode.value == "live"
        rationale = next_step_rationale(completed, step.tool)
        rationales.append(rationale)
        audit(run_id, "agent_decision", rationale)

        findings, status, ref, mode = run_adapter(adapter, target, use_live)
        raw_findings.extend(findings)
        add_tool_run(run_id, step.tool, mode.value, status, ref)
        audit(
            run_id,
            "tool_complete",
            f"{step.tool} mode={mode.value} status={status} findings={len(findings)}",
        )
        completed.append(step.tool)

    unified = correlate_and_dedupe(raw_findings)
    save_findings(run_id, unified)
    update_status(run_id, RunStatus.ANALYZED)
    audit(run_id, "correlation_complete", f"Unified findings: {len(unified)}")
    return unified, rationales


def prepare_validation_queue(findings: list[UnifiedFinding]) -> list[dict]:
    """High/critical suspected items require human approval before active validation."""
    queue = []
    for f in findings:
        if f.severity in ("high", "critical") and f.validation_status != "confirmed":
            queue.append(
                {
                    "finding_id": f.id,
                    "title": f.title,
                    "proposed_action": "Controlled Metasploit module (lab-only, import/stub)",
                    "requires_approval": True,
                }
            )
    return queue
