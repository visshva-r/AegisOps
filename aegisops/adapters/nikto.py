from __future__ import annotations

import re
from pathlib import Path

from aegisops.adapters.base import ToolAdapter
from aegisops.config import FIXTURES_DIR
from aegisops.models import FindingKind, RawFinding, ToolMode


class NiktoAdapter(ToolAdapter):
    name = "Nikto"
    default_mode = ToolMode.IMPORT

    def run(self, target: str, use_live: bool) -> tuple[list[RawFinding], str, str]:
        path = FIXTURES_DIR / "nikto_sample.txt"
        status = "import_fixture"
        return self._parse(path, target), status, str(path)

    def _parse(self, path: Path, target: str) -> list[RawFinding]:
        findings: list[RawFinding] = []
        text = path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            m = re.search(r"\+ (.+)", line)
            if not m:
                continue
            issue = m.group(1).strip()
            sev = "medium"
            if "OSVDB" in issue or "outdated" in issue.lower():
                sev = "medium"
            if "directory indexing" in issue.lower():
                sev = "high"
            findings.append(
                RawFinding(
                    source_tool="Nikto",
                    asset=f"http://{target}:8080",
                    title=issue[:120],
                    description=issue,
                    severity=sev,
                    evidence_ref=str(path),
                    raw_snippet=line.strip(),
                    confidence=0.85,
                    kind=FindingKind.OBSERVED,
                )
            )
        return findings
