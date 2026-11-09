# AegisOps — Final Submission Pack (Phase 3 Master Record)

**Evaluation Date:** 2026-11-09  
**Product:** AegisOps — AI Unified VAPT Agent  
**Hackathon:** DataOps Innovation Hackathon 2026  
**Problem Statement:** Problem Statement 1 (AI Unified VAPT Agent)  
**Live Target Reference Run ID:** `0ef8cf7c-de50-40fe-a2e3-38ffe4aabff9`  
**Application Endpoint:** `http://127.0.0.1:8000/`

---

## 1. Submission Verdict
### **READY FOR UNSTOP: YES**
AegisOps satisfies all judging criteria, safety guardrails, technical capabilities, and presentation deliverables. The application runs locally with sub-second responsiveness, enforces strict scope boundaries, provides multi-tool correlation, and generates client-ready PDF documentation.

---

## 2. Browser Walkthrough Scene List (B0 → B5)

| Scene | Target URL | UI Action & Verification | Screenshot Artifact |
|:---|:---|:---|:---|
| **B0: Home & Matrix** | `http://127.0.0.1:8000/` | Load homepage; observe dark-mode styling, version `v0.1.0`, 7-row Integration Matrix with colored badges, and Recent Lab Runs table. | `Project/evidence/demo/shot1_home_recent.png` |
| **B1: Scope Rejection** | `http://127.0.0.1:8000/assessments` | Enter unauthorized target `8.8.8.8`; click Submit; observe immediate HTTP 400 rejection with red error alert and 0 persisted DB records. | `Project/evidence/demo/shot2_scope_rejection.png` |
| **B2: Authorized Plan** | `http://127.0.0.1:8000/assessments` | Enter `lab.vapt.local` and natural-language goal; observe green scope confirmation banner, badge `status-planned`, and 3-step adaptive plan. | `Project/evidence/demo/shot3_planned_plan.png` |
| **B3: Orchestration & Gate** | `http://127.0.0.1:8000/assessments/{id}` | Click "Execute approved scan orchestration"; observe Tool Runs table (3 tools mapped to `fixtures/`), 15 unified findings, amber warning banner, and Human Approval card. | `Project/evidence/demo/shot4_awaiting_approval.png` |
| **B4: Human Approval** | `http://127.0.0.1:8000/assessments/{id}` | Enter note *"Demo approval for hackathon video"*; click Approve; observe green completion banner, badge `status-complete`, dismissed approval card, and logged audit events. | `Project/evidence/demo/shot5_complete_audit_pdf.png` |
| **B5: PDF & Persistence** | `http://127.0.0.1:8000/` | Download `aegisops-vapt-0ef8cf7c.pdf` (7,933 bytes); click "← New assessment"; verify Run `0ef8cf7c` appears in Recent Lab Runs with status `complete`. | `Project/evidence/demo/B5_extra.png` |

---

## 3. GitHub README Compliance Checklist

- [x] **Project Overview:** Clear statement addressing DataOps Innovation Hackathon 2026 Problem Statement 1.
- [x] **Judge Checklist Mapping:** Items 1–7 explicitly called out with corresponding solution features.
- [x] **Quick Start Instructions:** Step-by-step commands to create venv, install dependencies, and launch via `python run.py`.
- [x] **Authorized Targets Whitelist:** Clear documentation of allowed lab targets (`lab.vapt.local`, `10.10.10.10`, `localhost`, `10.10.*`).
- [x] **Sample Fixture Lineage:** Transparent listing of `nmap_sample.xml`, `nikto_sample.txt`, and `zap_sample.json`.
- [x] **Integration Matrix Reference:** Documented links to `INTEGRATION_MATRIX.md` and homepage UI table.
- [x] **Safety & Ethics Section:** Explicit affirmations regarding zero autonomous exploitation and human-in-the-loop oversight.
- [x] **Open Source License:** MIT License included.

---

## 4. Evaluation Rubric Narrative

### A. AI Reasoning & Adaptive Planning (20 Points)
- **Dynamic Plan Synthesis:** Rather than executing static hard-coded scripts, `aegisops/agent/planner.py` evaluates analyst keywords (`web`, `network`, `api`, `recon`) to select tools and construct execution order.
- **Contextual Next-Step Rationale:** Every planned stage carries an explicit rationale justifying its execution (e.g., executing Nmap first to supply open port context to Nikto, preventing blind brute-forcing).
- **Runtime Agent Decisions:** As orchestration proceeds, the pipeline evaluates completed tools and logs sequential `agent_decision` events into the audit trail.

### B. Safety, Guardrails & Governance (10 Points)
- **Pre-Execution Scope Enforcement:** Targets are normalized (stripping schemas, ports, and subpaths) and validated against strict lab allowlists. Non-compliant hosts trigger HTTP 400 before creating database records.
- **Mandatory Human-in-the-Loop Validation Gate:** The orchestrator automatically halts when high or critical findings are detected, presenting an approval form requiring analyst confirmation before any validation actions occur.
- **Non-Autonomous Exploitation:** Metasploit actions are strictly restricted to simulation stubs (`metasploit_stub`) to prevent accidental service disruption or unauthorized intrusion.

### C. Findings Correlation, Normalization & Confidence (15 Points)
- **Multi-Source Normalization:** Ingests disparate tool schemas (Nmap XML, Nikto text outputs, OWASP ZAP JSON) into a unified Pydantic schema (`UnifiedFinding`).
- **Cryptographic Deduplication:** Findings are hashed via SHA256 over normalized title and asset coordinates, merging duplicate alerts across tools.
- **Confidence Scoring & Source Validation:** Single-tool detections receive baseline confidence (0.85); multi-tool correlations trigger automatic confidence boosts (up to 0.99) and transition status from `suspected` to `correlated`.
- **Epistemic Labeling:** Every vulnerability is explicitly tagged as `observed` (directly confirmed by scanner output) or `inferred` (synthesized from configuration context).

---

## 5. "Do-Not-Claim" Transparency Rules

To maintain 100% integrity before the judging panel, the presenter must adhere to the following statements:
1. **Do NOT claim live Nessus scanning:** Nessus is marked **"Planned"** in the matrix and API pending enterprise licensing.
2. **Do NOT claim live OpenVAS execution:** OpenVAS is marked **"Planned"** as a future infrastructure adapter.
3. **Do NOT claim live Burp Suite active scanning:** Burp Suite is marked **"Import"** for planned manual exports only.
4. **Do NOT claim autonomous Metasploit exploitation:** Metasploit integration is strictly an import/simulation stub governed by human approval.
5. **Do NOT claim live Nmap scans when binaries are missing:** If Nmap is not installed on the host system PATH, the app honestly records status `import_fixture` rather than claiming a live execution succeeded.

---

## 6. Appendix: Complete Browser Walk Execution Logs

```text
[B0] Clicked: (none, load only)
     Saw: h1='AegisOps', version='AI-powered unified VAPT agent · authorized lab assessments only · v0.1.0', matrix rows=7, recent runs=5
     Screenshot: yes (shot1_home_recent.png)

[B1] Clicked: Submit 8.8.8.8 via form submit
     Saw: URL='http://127.0.0.1:8000/assessments', alert='Target '8.8.8.8' is outside authorized lab scope. Allowed: 10.10.10.10, 127.0.0.1, lab.vapt.local, localhost or private lab-CIDR.'
     Screenshot: yes (shot2_scope_rejection.png)

[B2] Clicked: Submit lab.vapt.local
     Saw: run_id='0ef8cf7c-de50-40fe-a2e3-38ffe4aabff9', badge='tag status-planned : planned', scope='Scope validated for authorized lab target: lab.vapt.local', plan steps=3
     Screenshot: yes (shot3_planned_plan.png)

[B3] Clicked: Execute approved scan orchestration
     Saw: badge='tag status-awaiting_approval : awaiting_approval', tool_rows=3, findings=15, warn='High-severity findings detected · approve validation to finalize the audit trail before client delivery.', approval='Human approval required', hint='Draft PDF available · approval events are appended after you approve or deny validation.'
     Screenshot: yes (shot4_awaiting_approval.png)

[B4] Clicked: Approve validation (note: 'Demo approval for hackathon video')
     Saw: badge='tag status-complete : complete', banner='Assessment completed · Human validation approval logged to audit trail.', approval_hidden=True, audit_entries=13, hint='Final report includes correlated findings, tool traceability, and audit/approval events.'
     Screenshot: yes (shot5_complete_audit_pdf.png)

[B5] Clicked: PDF download + return home
     Saw: PDF saved (7933 bytes), first recent row='0ef8cf7c…  lab.vapt.local  complete  2026-11-09T15:43:17'
     Screenshot: yes (B5_extra.png)
```

