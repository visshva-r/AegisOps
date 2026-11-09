# AegisOps integration status matrix

| Tool | Status | Demo behavior | Notes |
|------|--------|---------------|-------|
| Nmap | **Live** | Runs `nmap` if on PATH; falls back to `fixtures/nmap_sample.xml` | Network recon |
| Nikto | **Import** | Parses `fixtures/nikto_sample.txt` | No live Nikto misrepresentation |
| OWASP ZAP | **Import** | Parses `fixtures/zap_sample.json` | Web/API findings |
| Nessus | Planned | Not executed | API when license available |
| OpenVAS / Greenbone | Planned | Not executed | Future adapter |
| Burp Suite | Import | Planned | Export-only integration |
| Metasploit | Import | Human-approved stub only | Never autonomous |

## Transparency

- Live vs import is recorded per tool run in SQLite and shown in the UI and PDF.
- Failed live runs fall back to fixtures with status `live_failed_using_fixture`.
