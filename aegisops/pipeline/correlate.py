from __future__ import annotations

import hashlib
import uuid
from collections import defaultdict

from aegisops.models import FindingKind, RawFinding, UnifiedFinding

SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1, "info": 0}
SEVERITY_TO_CVSS = {"critical": 9.5, "high": 8.0, "medium": 5.5, "low": 3.0, "info": 0.0}


def _fingerprint(f: RawFinding) -> str:
    key = f"{f.title.lower()}|{f.asset.lower()}"
    return hashlib.sha256(key.encode()).hexdigest()[:16]


def correlate_and_dedupe(raw: list[RawFinding]) -> list[UnifiedFinding]:
    buckets: dict[str, list[RawFinding]] = defaultdict(list)
    for r in raw:
        buckets[_fingerprint(r)].append(r)

    unified: list[UnifiedFinding] = []
    for items in buckets.values():
        primary = max(items, key=lambda x: SEVERITY_ORDER.get(x.severity, 0))
        assets = sorted({i.asset for i in items})
        sources = sorted({i.source_tool for i in items})
        evidence_refs = sorted({i.evidence_ref for i in items})
        conf = min(0.99, sum(i.confidence for i in items) / len(items) + 0.05 * (len(sources) - 1))
        validation = "correlated" if len(sources) > 1 else "suspected"
        sev = primary.severity
        for i in items:
            if SEVERITY_ORDER.get(i.severity, 0) > SEVERITY_ORDER.get(sev, 0):
                sev = i.severity
        remediation = _remediation_hint(primary.title, sev)
        unified.append(
            UnifiedFinding(
                id=str(uuid.uuid4()),
                title=primary.title,
                description=primary.description,
                assets=assets,
                severity=sev,
                cvss_estimate=SEVERITY_TO_CVSS.get(sev),
                cve=primary.cve,
                sources=sources,
                evidence_refs=evidence_refs,
                confidence=round(conf, 2),
                validation_status=validation,
                kind=primary.kind if all(i.kind == FindingKind.OBSERVED for i in items) else FindingKind.INFERRED,
                remediation=remediation,
            )
        )

    unified.sort(
        key=lambda x: (
            -SEVERITY_ORDER.get(x.severity, 0),
            -x.confidence,
            x.title,
        )
    )
    return unified


def _remediation_hint(title: str, severity: str) -> str:
    t = title.lower()
    if "directory indexing" in t:
        return "Disable directory listing and restrict exposed paths."
    if "xss" in t or "cross site" in t:
        return "Encode output, apply CSP, and validate inputs server-side."
    if "header" in t and "missing" in t:
        return "Add security headers (CSP, X-Frame-Options, HSTS as applicable)."
    if "port" in t and "open" in t:
        return "Close unnecessary services or restrict access with firewall rules."
    if severity in ("high", "critical"):
        return "Prioritize patch or compensating control within 7 days."
    return "Review configuration and apply vendor hardening guidance."
