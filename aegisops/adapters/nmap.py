from __future__ import annotations

import shutil
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from aegisops.adapters.base import ToolAdapter
from aegisops.config import FIXTURES_DIR
from aegisops.models import FindingKind, RawFinding, ToolMode


class NmapAdapter(ToolAdapter):
    name = "Nmap"
    default_mode = ToolMode.LIVE

    def run(self, target: str, use_live: bool) -> tuple[list[RawFinding], str, str]:
        fixture = FIXTURES_DIR / "nmap_sample.xml"
        out_path = FIXTURES_DIR / f"nmap_live_{target.replace('.', '_')}.xml"
        ref = str(fixture)

        if use_live and shutil.which("nmap"):
            try:
                subprocess.run(
                    [
                        "nmap",
                        "-sV",
                        "-T4",
                        "--top-ports",
                        "20",
                        "-oX",
                        str(out_path),
                        target,
                    ],
                    check=True,
                    timeout=120,
                    capture_output=True,
                )
                ref = str(out_path)
                status = "completed_live"
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as exc:
                status = f"live_failed_using_fixture: {exc}"
        else:
            status = "import_fixture"

        return self._parse_xml(ref, target), status, ref

    def _parse_xml(self, path: str, target: str) -> list[RawFinding]:
        findings: list[RawFinding] = []
        root = ET.parse(path).getroot()
        for host in root.findall("host"):
            addr = host.find("address")
            asset = addr.get("addr") if addr is not None else target
            for port in host.findall(".//port"):
                state = port.find("state")
                if state is not None and state.get("state") != "open":
                    continue
                portid = port.get("portid", "?")
                proto = port.get("protocol", "tcp")
                svc = port.find("service")
                svc_name = svc.get("name", "unknown") if svc is not None else "unknown"
                findings.append(
                    RawFinding(
                        source_tool="Nmap",
                        asset=f"{asset}:{portid}/{proto}",
                        title=f"Open port {portid}/{proto} ({svc_name})",
                        description=f"Service {svc_name} detected on {asset}:{portid}/{proto}.",
                        severity="low" if svc_name in ("http", "https") else "info",
                        evidence_ref=path,
                        raw_snippet=f"port={portid} service={svc_name}",
                        confidence=0.95,
                        kind=FindingKind.OBSERVED,
                    )
                )
        return findings
