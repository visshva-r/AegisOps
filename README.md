# AegisOps

**AegisOps** is a conversational AI-assisted **Unified VAPT Agent** built for the DataOps Innovation Hackathon 2026 (Problem Statement 1).

**Repository:** [github.com/visshva-r/AegisOps](https://github.com/visshva-r/AegisOps)

It guides an **authorized lab assessment** from scope validation through multi-tool ingestion, AI correlation, risk prioritization, human approval for active validation, and a client-ready PDF report.

## Features (judge checklist)

- Natural-language analyst request + **scope enforcement** (lab targets only)
- **Adaptive assessment plan** with per-tool rationale
- **Three tool integrations**: Nmap (live if installed, else fixture), Nikto (import), OWASP ZAP (import)
- Normalization, deduplication, cross-tool correlation, confidence scoring
- **Human-in-the-loop** approval before Metasploit-style active validation (stub/import-only)
- Full **audit trail** + downloadable **VAPT PDF**
- Honest **integration status matrix** (Live / Import / Planned)

## Quick start

```bash
git clone https://github.com/visshva-r/AegisOps.git
cd AegisOps
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Open http://127.0.0.1:8000

### Demo path (video/PPT)

1. Submit request for `lab.vapt.local`
2. Review agent plan
3. **Execute approved scan orchestration**
4. Inspect correlated findings and tool traceability
5. **Approve** or deny human validation gate
6. **Download VAPT PDF**

## Authorized targets

- `lab.vapt.local`
- `10.10.10.10`
- `localhost` / `127.0.0.1`
- Hosts under `10.10.*` or `192.168.*`

Out-of-scope targets are rejected with an audit event.

## Fixtures

Sample outputs in `fixtures/` ensure reliable demos without live scanners:

- `nmap_sample.xml`
- `nikto_sample.txt`
- `zap_sample.json`

## Integration matrix

See [INTEGRATION_MATRIX.md](./INTEGRATION_MATRIX.md) and the in-app table on the home page.

## Tech stack

- Python 3.11+, FastAPI, SQLite, Jinja2, ReportLab
- Rule-based adaptive planner (LLM-ready extension point in `aegisops/agent/planner.py`)

## Safety & ethics

- No unauthorized scanning
- No autonomous exploitation
- Evidence vs inference labeled on findings
- Human approval required for consequential actions

## License

MIT — hackathon submission. Third-party tools (Nmap, Nikto, ZAP, etc.) remain subject to their own licenses.
