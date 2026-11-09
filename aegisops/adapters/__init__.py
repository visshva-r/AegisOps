from aegisops.adapters.base import run_adapter
from aegisops.adapters.nikto import NiktoAdapter
from aegisops.adapters.nmap import NmapAdapter
from aegisops.adapters.zap import ZapAdapter

ADAPTERS = {
    "Nmap": NmapAdapter(),
    "Nikto": NiktoAdapter(),
    "OWASP ZAP": ZapAdapter(),
}

__all__ = ["ADAPTERS", "run_adapter"]
