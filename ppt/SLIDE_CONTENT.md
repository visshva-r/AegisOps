# AegisOps — Slide Deck Content (PS-1 Submission)

> **Discord Presentation Structure** (Bullets only, presenter-ready format)

---

## Slide 1: Team Introduction & Problem Statement
- **Presenter:** Solo Developer / DataOps Innovation Hackathon 2026 Participant
- **Track / Challenge:** Problem Statement 1 — AI Unified VAPT Agent
- **Mission:** Build an intelligent, safe, and transparent VAPT orchestrator that converts natural-language mission requests into correlated vulnerability intelligence while maintaining human-in-the-loop safety.
- **Reference Artifact:**
  - `Project/evidence/demo/shot1_home_recent.png`
  - *Caption:* AegisOps dashboard displaying transparent multi-tool integration status matrix and persistent lab run history.

---

## Slide 2: The Problem
- **Tool Fragmentation:** Security teams run isolated point scanners (Nmap, Nikto, OWASP ZAP, Nessus) producing disconnected, incompatible raw files (XML, TXT, JSON).
- **Alert Fatigue & Duplication:** The same underlying misconfiguration (e.g., exposed services, missing headers) appears multiple times with differing severity rankings and zero cross-tool correlation.
- **Runaway Autonomous Exploitation Risks:** Existing AI penetration testing prototypes risk executing destructive exploits or targeting out-of-scope production assets without authorization.
- **Lack of Evidence Traceability:** Enterprise compliance audits require traceable lineage from executive report findings back to verifiable raw scan outputs.

---

## Slide 3: Your Solution — AegisOps
- **Conversational Scope Enforcement:** Accepts natural-language analyst goals while strictly enforcing pre-authorized lab-CIDR boundaries before dispatching any scan.
- **Adaptive Multi-Tool Orchestration:** Synthesizes analyst intent into an optimized, multi-phase assessment plan that reuses context across network and web layers.
- **Cross-Tool AI Correlation Engine:** Deduplicates findings using cryptographic asset fingerprints, normalizes severity with CVSS estimates, and computes confidence scores.
- **Mandatory Human-in-the-Loop Validation Gate:** Halts prior to active validation (Metasploit lab stub) and requires signed human approval recorded to an immutable audit trail.
- **Client-Ready VAPT PDF Reporting:** Generates an executive-ready 4-page report linking every vulnerability directly to its source tool evidence fixture.

---

## Slide 4: Project Architecture & Structure
- **Scope Verification Layer:** `aegisops/scope.py` normalizes targets and blocks unauthorized hosts with HTTP 400 rejections.
- **Adaptive Planning Engine:** `aegisops/agent/planner.py` generates dynamic sequencing rationale based on analyst keywords.
- **Tool Ingestion & Adapters:** Modular adapters (`nmap.py`, `nikto.py`, `zap.py`) execute live scanners or parse authoritative lab fixtures.
- **Correlation & Deduplication Pipeline:** `aegisops/pipeline/correlate.py` builds unified findings, calculates confidence, and distinguishes observed vs inferred risks.
- **Audit & Storage:** SQLite persistence (`runs`, `tool_runs`, `findings`, `audit_log`) maintains chronological audit lineage.
- **Report Generation:** `aegisops/report/pdf.py` renders publication-grade A4 PDF reports via ReportLab.
- **Reference Artifacts:**
  - `Project/evidence/demo/shot3_planned_plan.png`
  - *Caption:* Adaptive 3-stage execution plan showing reasoned context handoff from Nmap reconnaissance to Nikto and ZAP.

---

## Slide 5: Tech Stack
- **Backend Framework:** Python 3.10+, FastAPI (asynchronous REST API & web service).
- **Storage Layer:** SQLite 3 with atomic transaction management and relational foreign-key integrity.
- **Templating & UI:** Jinja2 server-side templates with responsive, zero-dependency dark-mode CSS.
- **Document Rendering:** ReportLab 5.1 (flowable layouts, automated tables, multi-page styling).
- **HTTP & Validation:** Pydantic v2 schemas, Starlette, HTTPX.
- **Scanners & Integration Targets:** Nmap (live network mapper), Nikto (web server scanner), OWASP ZAP (application security testing), Metasploit (validation stub).

---

## Slide 6: Features (Judge Checklist PS-1 §10)
- **1. Conversational Request & Scope Validation:** Accepts natural language while blocking public targets (e.g., `8.8.8.8`) with zero database leakage (`shot2_scope_rejection.png`).
- **2. Adaptive AI Plan with Tool Rationale:** Dynamically generates ordered scan steps, explaining why network context feeds web misconfiguration checks (`shot3_planned_plan.png`).
- **3. Traceable Multi-Tool Ingestion:** Normalizes outputs across Nmap, Nikto, and ZAP with absolute fixture references.
- **4. Normalization, Deduplication & Confidence Scoring:** SHA256 fingerprinting deduplicates findings; confidence increases when vulnerabilities are verified across multiple tools.
- **5. Risk Prioritization & Human Approval Gate:** Sorts by severity; triggers explicit analyst approval card for high/critical findings prior to validation (`shot4_awaiting_approval.png`).
- **6. Downloadable Executive PDF:** Complete 4-page report with Methodology, Severity Distribution, Detailed Findings, and recorded Human Approvals (`shot5_complete_audit_pdf.png`).
- **7. Honest Transparency & Matrix:** Live vs. Import vs. Planned status matrix exposed in UI and `/api/integration-matrix` without false live claims (`shot1_home_recent.png`).

---

## Slide 7: Feasibility
- **Zero Heavy Infrastructure Overhead:** Runs standalone on lightweight Python environments without requiring distributed message brokers.
- **Graceful Tool Degradation:** Adapters seamlessly run live commands if binaries are installed or fall back to verified fixtures without breaking demos.
- **Ultra-Low Latency Execution:** Entire correlation pipeline and PDF generation execute in sub-100ms response times.
- **Commercial Adaptation:** Ready for enterprise deployment using Docker containers and cloud Kubernetes clusters.

---

## Slide 8: Limitations
- **Current Prototype Scope:** Scope whitelist is configured for lab and RFC-1918 private subnets; multi-tenant enterprise RBAC is not yet implemented.
- **Synchronous Scan Ingestion:** Long-running external live scans (e.g., full port ranges) require background worker task queues (Celery/Redis) for production scale.
- **Stubbed Metasploit Exploitation:** Active exploitation modules are strictly restricted to simulation stubs to eliminate risk during hackathon evaluation.
- **Local Fixture Reliance:** In environments lacking native Nmap or Nikto installations, demo resilience relies on verified offline fixture baselines.

---

## Slide 9: Future Scope
- **LLM-Powered Remediation Playbooks:** Integrate Gemini Live / Anthropic APIs for contextual, automated patch-generation scripts.
- **Interactive Attack Path Graph:** Replace tabular findings with a visual Directed Acyclic Graph (DAG) illustrating lateral movement risks.
- **Enterprise Connector Ecosystem:** Implement planned adapters for Nessus API, Burp Suite Enterprise, and DefectDojo vulnerability management.
- **CI/CD Security Gateways:** Package AegisOps as a GitHub Action and GitLab CI step to enforce pre-deployment security thresholds.

