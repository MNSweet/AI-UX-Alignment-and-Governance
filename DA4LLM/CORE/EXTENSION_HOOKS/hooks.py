"""Declared extension points; absent GOVERNANCE is a valid no-op."""

from __future__ import annotations

from typing import Any

from ..model import GovernanceHooks


LIFECYCLE_HOOKS = (
    "PRE_EXECUTION",
    "PRE_CAPABILITY",
    "POST_CAPABILITY",
    "PRE_OUTPUT",
    "POST_OUTPUT",
)


def apply_hook(governance: GovernanceHooks | None, hook: str, context: dict[str, Any]) -> None:
    if hook not in LIFECYCLE_HOOKS:
        raise ValueError(f"Unknown lifecycle hook: {hook}")
    if governance is not None:
        governance.apply(hook, context)
