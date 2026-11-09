from __future__ import annotations

import json
from pathlib import Path

from aegisops.adapters.base import ToolAdapter
from aegisops.config import FIXTURES_DIR
from aegisops.models import FindingKind, RawFinding, ToolMode


class ZapAdapter(ToolAdapter):
    name = "OWASP ZAP"
    default_mode = ToolMode.IMPORT

    def run(self, target: str, use_live: bool) -> tuple[list[RawFinding], str, str]:
        path = FIXTURES_DIR / "zap_sample.json"
        status = "import_fixture"
        return self._parse(path, target), status, str(path)

    def _parse(self, path: Path, target: str) -> list[RawFinding]:
        data = json.loads(path.read_text(encoding="utf-8"))
        findings: list[RawFinding] = []
        for site in data.get("site", []):
            asset = site.get("@name", f"http://{target}")
            for alert in site.get("alerts", []):
                risk = (alert.get("riskdesc") or "Informational").lower()
                sev_map = {
                    "high": "high",
                    "medium": "medium",
                    "low": "low",
                    "informational": "info",
                }
                sev = "info"
                for k, v in sev_map.items():
                    if k in risk:
                        sev = v
                        break
                findings.append(
                    RawFinding(
                        source_tool="OWASP ZAP",
                        asset=asset,
                        title=alert.get("name", "Web alert"),
                        description=alert.get("desc", "")[:500],
                        severity=sev,
                        cve=alert.get("reference", "").split("\n")[0] if alert.get("reference") else None,
                        evidence_ref=str(path),
                        raw_snippet=alert.get("solution", "")[:200],
                        confidence=0.88,
                        kind=FindingKind.OBSERVED,
                    )
                )
        return findings
