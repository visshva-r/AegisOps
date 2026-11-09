from __future__ import annotations

from abc import ABC, abstractmethod

from aegisops.models import RawFinding, ToolMode


class ToolAdapter(ABC):
    name: str
    default_mode: ToolMode

    @abstractmethod
    def run(self, target: str, use_live: bool) -> tuple[list[RawFinding], str, str]:
        """Returns findings, run status, output reference."""

    def mode_for(self, use_live: bool) -> ToolMode:
        if use_live and self.default_mode == ToolMode.LIVE:
            return ToolMode.LIVE
        return ToolMode.IMPORT


def run_adapter(
    adapter: ToolAdapter, target: str, use_live: bool
) -> tuple[list[RawFinding], str, str, ToolMode]:
    mode = adapter.mode_for(use_live)
    findings, status, ref = adapter.run(target, use_live=use_live)
    return findings, status, ref, mode
