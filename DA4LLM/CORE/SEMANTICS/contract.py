"""Loading and deterministic type resolution for semantic contracts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..model import Diagnostic, Literal, SemanticContract, ValidationError


SUPPORTED_TYPES = {"string", "integer", "float", "boolean", "null"}


def load_semantics(path: Path) -> SemanticContract:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError([Diagnostic("SEMANTIC_LOAD_FAILED", str(error), "error")]) from error
    if not isinstance(data, dict):
        raise ValidationError([
            Diagnostic("SEMANTIC_SCHEMA_INVALID", "Semantic contract must be a JSON object", "error")
        ])
    required = {"module", "module_version", "variables", "operations"}
    missing = sorted(required - data.keys())
    if missing:
        raise ValidationError([
            Diagnostic("SEMANTIC_SCHEMA_INVALID", f"Missing semantic fields: {', '.join(missing)}", "error")
        ])
    if not isinstance(data["variables"], dict) or not isinstance(data["operations"], dict):
        raise ValidationError([
            Diagnostic("SEMANTIC_SCHEMA_INVALID", "variables and operations must be objects", "error")
        ])
    if not isinstance(data["module"], str) or not isinstance(data["module_version"], str):
        raise ValidationError([
            Diagnostic("SEMANTIC_SCHEMA_INVALID", "module and module_version must be strings", "error")
        ])
    return SemanticContract(
        module=data["module"],
        module_version=data["module_version"],
        variables=data["variables"],
        operations=data["operations"],
        source=path,
    )


def coerce_literal(literal: Literal, target_type: str | None) -> Any:
    """Apply semantic type first; otherwise retain the CORE lexical default."""
    if target_type is None or target_type == literal.lexical_type:
        return literal.value
    try:
        if target_type == "string":
            if literal.lexical_type == "boolean":
                return literal.raw.lower()
            if literal.lexical_type == "null":
                return "null"
            return str(literal.value)
        if target_type == "integer":
            if literal.lexical_type in {"boolean", "null"}:
                raise ValueError(f"{literal.lexical_type} cannot become an integer")
            numeric = float(literal.value)
            if not numeric.is_integer():
                raise ValueError("fractional value cannot become an integer")
            return int(numeric)
        if target_type == "float":
            if literal.lexical_type in {"boolean", "null"}:
                raise ValueError(f"{literal.lexical_type} cannot become a float")
            return float(literal.value)
        if target_type == "boolean":
            text = str(literal.value).lower()
            if text not in {"true", "false"}:
                raise ValueError("boolean must be true or false")
            return text == "true"
        if target_type == "null" and literal.value is None:
            return None
    except (TypeError, ValueError) as error:
        raise ValidationError([
            Diagnostic(
                "SEMANTIC_TYPE_MISMATCH",
                f"Cannot resolve {literal.raw!r} as {target_type}: {error}",
                "error",
                literal.line,
            )
        ]) from error
    raise ValidationError([
        Diagnostic(
            "SEMANTIC_TYPE_MISMATCH",
            f"Cannot resolve lexical type {literal.lexical_type} as {target_type}",
            "error",
            literal.line,
        )
    ])
