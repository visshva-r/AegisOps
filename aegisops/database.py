from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from aegisops.config import DB_PATH
from aegisops.models import (
    AssessmentPlan,
    AssessmentRequest,
    RunStatus,
    UnifiedFinding,
)


def _ensure_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS runs (
                id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                analyst_request TEXT NOT NULL,
                exclusions TEXT,
                status TEXT NOT NULL,
                plan_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                action TEXT NOT NULL,
                detail TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES runs(id)
            );
            CREATE TABLE IF NOT EXISTS tool_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT NOT NULL,
                tool TEXT NOT NULL,
                mode TEXT NOT NULL,
                status TEXT NOT NULL,
                output_ref TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES runs(id)
            );
            CREATE TABLE IF NOT EXISTS findings (
                id TEXT PRIMARY KEY,
                run_id TEXT NOT NULL,
                data_json TEXT NOT NULL,
                FOREIGN KEY (run_id) REFERENCES runs(id)
            );
            """
        )


@contextmanager
def get_conn():
    _ensure_db()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_run(req: AssessmentRequest) -> str:
    run_id = str(uuid.uuid4())
    now = utc_now()
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO runs (id, target, analyst_request, exclusions, status, plan_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                req.target.strip(),
                req.analyst_request.strip(),
                req.exclusions,
                RunStatus.CREATED.value,
                None,
                now,
                now,
            ),
        )
    audit(run_id, "run_created", f"Target: {req.target}")
    return run_id


def audit(run_id: str, action: str, detail: str = "") -> None:
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO audit_log (run_id, action, detail, created_at) VALUES (?, ?, ?, ?)",
            (run_id, action, detail, utc_now()),
        )


def update_status(run_id: str, status: RunStatus) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE runs SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, utc_now(), run_id),
        )


def save_plan(run_id: str, plan: AssessmentPlan) -> None:
    with get_conn() as conn:
        conn.execute(
            "UPDATE runs SET plan_json = ?, status = ?, updated_at = ? WHERE id = ?",
            (json.dumps(plan.model_dump()), RunStatus.PLANNED.value, utc_now(), run_id),
        )
    audit(run_id, "plan_generated", plan.summary)


def add_tool_run(
    run_id: str, tool: str, mode: str, status: str, output_ref: str = ""
) -> None:
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO tool_runs (run_id, tool, mode, status, output_ref, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (run_id, tool, mode, status, output_ref, utc_now()),
        )


def save_findings(run_id: str, findings: list[UnifiedFinding]) -> None:
    with get_conn() as conn:
        conn.execute("DELETE FROM findings WHERE run_id = ?", (run_id,))
        for f in findings:
            conn.execute(
                "INSERT INTO findings (id, run_id, data_json) VALUES (?, ?, ?)",
                (f.id, run_id, json.dumps(f.model_dump())),
            )


def list_recent_runs(limit: int = 5) -> list[dict[str, Any]]:
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT id, target, status, created_at
            FROM runs
            ORDER BY datetime(created_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def load_run(run_id: str) -> dict[str, Any] | None:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,)).fetchone()
        if not row:
            return None
        audit_rows = conn.execute(
            "SELECT action, detail, created_at FROM audit_log WHERE run_id = ? ORDER BY id",
            (run_id,),
        ).fetchall()
        tool_rows = conn.execute(
            "SELECT tool, mode, status, output_ref, created_at FROM tool_runs WHERE run_id = ? ORDER BY id",
            (run_id,),
        ).fetchall()
        finding_rows = conn.execute(
            "SELECT data_json FROM findings WHERE run_id = ?",
            (run_id,),
        ).fetchall()
    plan = None
    if row["plan_json"]:
        plan = AssessmentPlan.model_validate(json.loads(row["plan_json"]))
    findings = [
        UnifiedFinding.model_validate(json.loads(r["data_json"])) for r in finding_rows
    ]
    return {
        "run_id": row["id"],
        "status": RunStatus(row["status"]),
        "target": row["target"],
        "analyst_request": row["analyst_request"],
        "exclusions": row["exclusions"] or "",
        "plan": plan,
        "tool_runs": [dict(r) for r in tool_rows],
        "findings": findings,
        "audit": [dict(r) for r in audit_rows],
    }
