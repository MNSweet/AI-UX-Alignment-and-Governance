"""Manifest, logic, and semantics validation for DA4LLM modules."""

from __future__ import annotations

import json
from pathlib import Path

from .LOGIC.PARSER import parse
from .SEMANTICS import coerce_literal, load_semantics
from .SEMANTICS.OPERATIONS import OPCODES
from .SEMANTICS.contract import SUPPORTED_TYPES
from .model import (
    CapabilityStatement,
    Diagnostic,
    ExecutionMode,
    ModuleManifest,
    ReturnStatement,
    SemanticState,
    SetStatement,
    ValidatedModule,
    ValidationError,
)


FORBIDDEN_SEMANTIC_KEYS = {"if", "then", "else", "steps", "sequence", "goto", "execute"}


def _module_path(base: Path, member: str, field: str) -> Path:
    resolved_base = base.resolve()
    resolved_member = (resolved_base / member).resolve()
    try:
        resolved_member.relative_to(resolved_base)
    except ValueError as error:
        raise ValidationError([
            Diagnostic(
                "MANIFEST_PATH_OUTSIDE_MODULE",
                f"Manifest field {field!r} must stay inside the module directory",
                "error",
            )
        ]) from error
    return resolved_member


def _read_manifest(path: Path) -> ModuleManifest:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValidationError([Diagnostic("MANIFEST_LOAD_FAILED", str(error), "error")]) from error
    if not isinstance(data, dict):
        raise ValidationError([
            Diagnostic("MANIFEST_SCHEMA_INVALID", "Manifest must be a JSON object", "error")
        ])
    required = {"module", "module_version", "logic"}
    missing = sorted(required - data.keys())
    if missing:
        raise ValidationError([
            Diagnostic("MANIFEST_SCHEMA_INVALID", f"Missing manifest fields: {', '.join(missing)}", "error")
        ])
    for field in required:
        if not isinstance(data[field], str) or not data[field]:
            raise ValidationError([
                Diagnostic("MANIFEST_SCHEMA_INVALID", f"Manifest field {field!r} must be a string", "error")
            ])
    base = path.parent
    semantic_name = data.get("semantics")
    if semantic_name is not None and (not isinstance(semantic_name, str) or not semantic_name):
        raise ValidationError([
            Diagnostic("MANIFEST_SCHEMA_INVALID", "Manifest field 'semantics' must be a string", "error")
        ])
    return ModuleManifest(
        module=data["module"],
        module_version=data["module_version"],
        logic_path=_module_path(base, data["logic"], "logic"),
        semantic_path=_module_path(base, semantic_name, "semantics") if semantic_name else None,
        source=path.resolve(),
    )


def load_module(manifest_path: Path | str, mode: ExecutionMode = ExecutionMode.NORMAL) -> ValidatedModule:
    manifest = _read_manifest(Path(manifest_path).resolve())
    try:
        logic = parse(manifest.logic_path.read_text(encoding="utf-8"), manifest.logic_path)
    except OSError as error:
        raise ValidationError([Diagnostic("LOGIC_LOAD_FAILED", str(error), "error")]) from error

    errors: list[Diagnostic] = []
    warnings: list[Diagnostic] = []
    if logic.name != manifest.module or logic.version != manifest.module_version:
        errors.append(Diagnostic(
            "MODULE_IDENTITY_MISMATCH",
            "Manifest and logic module names and versions must match exactly",
            "error",
        ))

    semantics = None
    if manifest.semantic_path:
        if not manifest.semantic_path.exists():
            errors.append(Diagnostic(
                "SEMANTIC_LOAD_FAILED",
                f"Manifest semantic file does not exist: {manifest.semantic_path.name}",
                "error",
            ))
        else:
            semantics = load_semantics(manifest.semantic_path)
            if semantics.module != manifest.module or semantics.module_version != manifest.module_version:
                errors.append(Diagnostic(
                    "SEMANTIC_VERSION_MISMATCH",
                    "Manifest, logic, and semantic module names and versions must match exactly",
                    "error",
                ))

    assigned: set[str] = set()
    used: set[str] = set()
    operations: set[str] = set()
    for statement in logic.statements:
        operations.add(statement.opcode)
        if statement.opcode not in OPCODES:
            errors.append(Diagnostic("UNKNOWN_OPCODE", statement.opcode, "error", statement.line))
        if isinstance(statement, SetStatement):
            assigned.add(statement.name)
        elif isinstance(statement, CapabilityStatement):
            if statement.payload_variable:
                used.add(statement.payload_variable)
                if statement.payload_variable not in assigned:
                    errors.append(Diagnostic(
                        "VARIABLE_UNDEFINED",
                        f"Capability payload variable {statement.payload_variable!r} is not assigned",
                        "error",
                        statement.line,
                    ))
            if statement.result_variable:
                assigned.add(statement.result_variable)
        elif isinstance(statement, ReturnStatement):
            used.add(statement.variable)
            if statement.variable not in assigned:
                errors.append(Diagnostic(
                    "VARIABLE_UNDEFINED",
                    f"Return variable {statement.variable!r} is not assigned",
                    "error",
                    statement.line,
                ))

    missing_variables: set[str] = set()
    missing_operations: set[str] = set()
    if semantics is None:
        semantic_state = SemanticState.ABSENT
        warnings.append(Diagnostic("SEMANTIC_ABSENT", "Module has no semantic contract"))
    else:
        missing_variables = (assigned | used) - semantics.variables.keys()
        missing_operations = operations - semantics.operations.keys()
        semantic_state = SemanticState.COMPLETE
        if missing_variables or missing_operations:
            semantic_state = SemanticState.PARTIAL
            details = []
            if missing_variables:
                details.append(f"variables: {', '.join(sorted(missing_variables))}")
            if missing_operations:
                details.append(f"operations: {', '.join(sorted(missing_operations))}")
            warnings.append(Diagnostic("SEMANTIC_PARTIAL", "Missing semantic entries for " + "; ".join(details)))
        contract_incomplete = False
        for variable, contract in semantics.variables.items():
            if not isinstance(contract, dict) or contract.get("type") not in SUPPORTED_TYPES:
                errors.append(Diagnostic(
                    "SEMANTIC_TYPE_INVALID",
                    f"Variable {variable!r} must declare a supported type",
                    "error",
                ))
            if not isinstance(contract, dict) or not contract.get("purpose"):
                contract_incomplete = True
                warnings.append(Diagnostic(
                    "SEMANTIC_PURPOSE_MISSING",
                    f"Variable {variable!r} has no stated purpose",
                ))
        for operation, contract in semantics.operations.items():
            if not isinstance(contract, dict):
                errors.append(Diagnostic(
                    "SEMANTIC_OPERATION_INVALID", f"Operation {operation!r} must be an object", "error"
                ))
                continue
            if not contract.get("meaning"):
                contract_incomplete = True
                warnings.append(Diagnostic(
                    "SEMANTIC_MEANING_MISSING",
                    f"Operation {operation!r} has no stated meaning",
                ))
            forbidden = FORBIDDEN_SEMANTIC_KEYS.intersection(key.lower() for key in contract)
            if forbidden:
                errors.append(Diagnostic(
                    "SEMANTIC_CONTAINS_LOGIC",
                    f"Operation {operation!r} contains procedural keys: {', '.join(sorted(forbidden))}",
                    "error",
                ))
        for variable in semantics.variables.keys() - (assigned | used):
            warnings.append(Diagnostic("SEMANTIC_VARIABLE_UNUSED", f"Variable {variable!r} is not used by logic"))
        if contract_incomplete and semantic_state is SemanticState.COMPLETE:
            semantic_state = SemanticState.PARTIAL
            warnings.append(Diagnostic(
                "SEMANTIC_PARTIAL",
                "Semantic entries are present but required type, purpose, or meaning fields are incomplete",
            ))
        for statement in logic.statements:
            if isinstance(statement, SetStatement) and statement.name in semantics.variables:
                variable_contract = semantics.variables[statement.name]
                target_type = variable_contract.get("type") if isinstance(variable_contract, dict) else None
                if target_type in SUPPORTED_TYPES:
                    try:
                        coerce_literal(statement.value, target_type)
                    except ValidationError as error:
                        errors.extend(error.diagnostics)

    if mode is ExecutionMode.STRICT and semantic_state is not SemanticState.COMPLETE:
        errors.append(Diagnostic(
            "SEMANTIC_REQUIRED",
            f"Strict mode requires SEMANTIC_COMPLETE, found {semantic_state.value}",
            "error",
        ))
    if errors:
        raise ValidationError(errors)
    visible_warnings = tuple(warnings if mode in {ExecutionMode.DEBUG, ExecutionMode.STRICT} else ())
    return ValidatedModule(manifest, logic, semantics, semantic_state, visible_warnings)
