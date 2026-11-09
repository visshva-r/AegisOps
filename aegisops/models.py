from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class RunStatus(str, Enum):
    CREATED = "created"
    PLANNED = "planned"
    SCANNING = "scanning"
    ANALYZED = "analyzed"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    COMPLETE = "complete"
    REJECTED = "rejected"


class ToolMode(str, Enum):
    LIVE = "live"
    IMPORT = "import"


class FindingKind(str, Enum):
    OBSERVED = "observed"
    INFERRED = "inferred"


class AssessmentRequest(BaseModel):
    analyst_request: str
    target: str
    exclusions: str = ""


class PlanStep(BaseModel):
    tool: str
    mode: ToolMode
    rationale: str
    order: int


class AssessmentPlan(BaseModel):
    steps: list[PlanStep]
    summary: str


class RawFinding(BaseModel):
    source_tool: str
    asset: str
    title: str
    description: str
    severity: str = "info"
    cve: str | None = None
    evidence_ref: str
    raw_snippet: str
    confidence: float = 0.75
    kind: FindingKind = FindingKind.OBSERVED


class UnifiedFinding(BaseModel):
    id: str
    title: str
    description: str
    assets: list[str]
    severity: str
    cvss_estimate: float | None = None
    cve: str | None = None
    sources: list[str]
    evidence_refs: list[str]
    confidence: float
    validation_status: str = "suspected"
    kind: FindingKind = FindingKind.OBSERVED
    remediation: str = ""


class ApprovalRequest(BaseModel):
    approved: bool
    note: str = ""


class RunStateResponse(BaseModel):
    run_id: str
    status: RunStatus
    target: str
    analyst_request: str
    plan: AssessmentPlan | None = None
    tool_runs: list[dict[str, Any]] = Field(default_factory=list)
    findings: list[UnifiedFinding] = Field(default_factory=list)
    audit: list[dict[str, Any]] = Field(default_factory=list)
    pending_validation: list[dict[str, Any]] = Field(default_factory=list)
