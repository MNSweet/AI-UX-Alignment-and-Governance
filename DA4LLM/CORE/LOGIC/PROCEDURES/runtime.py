"""Deterministic procedure execution for the DA4LLM CORE POC."""

from __future__ import annotations

from typing import Any

from ...CAPABILITIES import invoke_capability
from ...EXTENSION_HOOKS import apply_hook
from ...SEMANTICS import coerce_literal
from ...model import (
    CapabilityBridge,
    CapabilityStatement,
    Diagnostic,
    ExecutionError,
    ExecutionResult,
    GovernanceHooks,
    ReturnStatement,
    SetStatement,
    ValidatedModule,
)


def execute(
    module: ValidatedModule,
    bridge: CapabilityBridge | None = None,
    governance: GovernanceHooks | None = None,
) -> ExecutionResult:
    variables: dict[str, Any] = {}
    diagnostics = list(module.diagnostics)
    trace: list[str] = []
    output: Any = None

    context = {"module": module.logic.name, "version": module.logic.version, "variables": variables}
    apply_hook(governance, "PRE_EXECUTION", context)
    trace.append("PRE_EXECUTION")

    for statement in module.logic.statements:
        if isinstance(statement, SetStatement):
            target_type = None
            if module.semantics and statement.name in module.semantics.variables:
                target_type = module.semantics.variables[statement.name].get("type")
            variables[statement.name] = coerce_literal(statement.value, target_type)
            trace.append(f"SET:{statement.name}")
            continue

        if isinstance(statement, CapabilityStatement):
            payload = variables.get(statement.payload_variable) if statement.payload_variable else None
            capability_context = {
                **context,
                "capability": statement.capability,
                "payload": payload,
            }
            apply_hook(governance, "PRE_CAPABILITY", capability_context)
            trace.append(f"PRE_CAPABILITY:{statement.capability}")
            result = invoke_capability(bridge, statement.capability, payload, statement.line)
            capability_context["result"] = result
            apply_hook(governance, "POST_CAPABILITY", capability_context)
            trace.append(f"POST_CAPABILITY:{statement.capability}:{result.status}")
            if result.status == "unavailable":
                diagnostic = result.diagnostic or Diagnostic(
                    "CAPABILITY_UNAVAILABLE", statement.capability, "error", statement.line
                )
                if statement.on_unavailable == "CONTINUE":
                    diagnostic = Diagnostic(
                        diagnostic.code,
                        diagnostic.message,
                        "warning",
                        diagnostic.line,
                    )
                diagnostics.append(diagnostic)
                if statement.result_variable:
                    variables[statement.result_variable] = {
                        "status": result.status,
                        "capability": statement.capability,
                    }
                if statement.on_unavailable == "HALT":
                    raise ExecutionError(diagnostic)
            elif statement.result_variable:
                variables[statement.result_variable] = result.value
            continue

        if isinstance(statement, ReturnStatement):
            output = variables[statement.variable]
            output_context = {**context, "output": output}
            apply_hook(governance, "PRE_OUTPUT", output_context)
            trace.append("PRE_OUTPUT")
            output = output_context["output"]
            apply_hook(governance, "POST_OUTPUT", output_context)
            trace.append("POST_OUTPUT")
            break

    return ExecutionResult(output, dict(variables), tuple(diagnostics), tuple(trace))
