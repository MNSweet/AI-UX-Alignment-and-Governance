"""Provider-neutral capability boundary owned by CORE."""

from __future__ import annotations

from typing import Any

from ..model import CapabilityBridge, CapabilityResult, CapabilityUnavailable, Diagnostic


def invoke_capability(
    bridge: CapabilityBridge | None,
    capability: str,
    payload: Any,
    line: int,
) -> CapabilityResult:
    if bridge is None:
        diagnostic = Diagnostic(
            "CAPABILITY_UNAVAILABLE",
            f"No BRIDGE is present for capability {capability!r}",
            "error",
            line,
        )
        return CapabilityResult("unavailable", capability, diagnostic=diagnostic)
    try:
        return CapabilityResult("available", capability, bridge.call(capability, payload))
    except CapabilityUnavailable as error:
        diagnostic = Diagnostic("CAPABILITY_UNAVAILABLE", str(error), "error", line)
        return CapabilityResult("unavailable", capability, diagnostic=diagnostic)
