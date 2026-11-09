from __future__ import annotations

from aegisops.models import AssessmentPlan, AssessmentRequest, PlanStep, ToolMode


def build_plan(req: AssessmentRequest, normalized_target: str) -> AssessmentPlan:
    """Evidence-driven adaptive plan based on request text and target type."""
    text = req.analyst_request.lower()
    web_focus = any(
        k in text for k in ("web", "api", "http", "application", "owasp", "xss", "csrf")
    )
    network_focus = any(
        k in text for k in ("network", "port", "service", "recon", "infrastructure", "host")
    )
    if not web_focus and not network_focus:
        web_focus = network_focus = True

    steps: list[PlanStep] = []
    order = 1

    if network_focus:
        steps.append(
            PlanStep(
                tool="Nmap",
                mode=ToolMode.LIVE,
                rationale=(
                    f"Discover open ports and services on {normalized_target} before deeper "
                    "web checks. Live scan if Nmap is available; otherwise import authorized fixture."
                ),
                order=order,
            )
        )
        order += 1

    if web_focus:
        steps.append(
            PlanStep(
                tool="Nikto",
                mode=ToolMode.IMPORT,
                rationale=(
                    "After service discovery, run web server misconfiguration checks. "
                    "Import-only in this prototype (no misrepresentation of commercial tooling)."
                ),
                order=order,
            )
        )
        order += 1
        steps.append(
            PlanStep(
                tool="OWASP ZAP",
                mode=ToolMode.IMPORT,
                rationale=(
                    "Correlate application-layer findings (headers, cookies, injection classes) "
                    "with Nikto/Nmap context for cross-tool evidence."
                ),
                order=order,
            )
        )
        order += 1

    summary = (
        f"Adaptive plan for '{normalized_target}': {len(steps)} tool stage(s) selected from "
        f"analyst intent ({'web+' if web_focus else ''}{'network' if network_focus else ''}). "
        "Each step explains why the next investigation is needed."
    )
    return AssessmentPlan(steps=steps, summary=summary)


def next_step_rationale(completed_tools: list[str], pending: str) -> str:
    if not completed_tools:
        return f"Starting with {pending} because no reconnaissance evidence exists yet."
    return (
        f"Prior tools ({', '.join(completed_tools)}) supplied asset/service context; "
        f"proceeding to {pending} to correlate web-layer risks without repeating network discovery."
    )
