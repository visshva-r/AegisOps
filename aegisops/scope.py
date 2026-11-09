from aegisops.config import ALLOWED_CIDR_HINTS, ALLOWED_TARGETS


class ScopeError(Exception):
    pass


def normalize_target(target: str) -> str:
    t = target.strip().lower()
    if t.startswith("http://"):
        t = t[7:]
    if t.startswith("https://"):
        t = t[8:]
    t = t.split("/")[0].split(":")[0]
    return t


def validate_scope(target: str, exclusions: str = "") -> tuple[str, str]:
    """Return normalized target and scope decision message."""
    host = normalize_target(target)
    if host not in ALLOWED_TARGETS and not any(
        host.startswith(prefix) for prefix in ALLOWED_CIDR_HINTS
    ):
        raise ScopeError(
            f"Target '{host}' is outside authorized lab scope. "
            f"Allowed: {', '.join(sorted(ALLOWED_TARGETS))} or private lab-CIDR."
        )
    return host, f"Scope validated for authorized lab target: {host}"


def is_action_in_scope(target: str) -> bool:
    try:
        validate_scope(target)
        return True
    except ScopeError:
        return False
