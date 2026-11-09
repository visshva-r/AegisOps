from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FIXTURES_DIR = BASE_DIR / "fixtures"
DB_PATH = BASE_DIR / "data" / "aegisops.db"

# Organizer-authorized lab targets only (sandbox)
ALLOWED_TARGETS = {
    "lab.vapt.local",
    "10.10.10.10",
    "127.0.0.1",
    "localhost",
}

ALLOWED_CIDR_HINTS = ("10.10.", "192.168.")

INTEGRATION_MATRIX = [
    {"tool": "Nmap", "status": "Live", "role": "Host/port/service discovery"},
    {"tool": "Nikto", "status": "Import", "role": "Web server checks (fixture/import)"},
    {"tool": "OWASP ZAP", "status": "Import", "role": "Web/API scan results (JSON import)"},
    {"tool": "Nessus", "status": "Planned", "role": "API integration when license available"},
    {"tool": "OpenVAS", "status": "Planned", "role": "Infrastructure scanning"},
    {"tool": "Burp Suite", "status": "Import", "role": "Manual export integration (planned)"},
    {"tool": "Metasploit", "status": "Import", "role": "Human-approved lab validation only"},
]
