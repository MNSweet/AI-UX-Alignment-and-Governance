"""Command-line entry point for validating and running DA4LLM POC modules."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .LOGIC.PROCEDURES import execute
from .model import DA4LLMError, ExecutionMode
from .validator import load_module


def _diagnostics(items):
    return [asdict(item) for item in items]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DA4LLM CORE proof-of-concept validator")
    parser.add_argument("command", choices=("validate", "run"))
    parser.add_argument("manifest")
    parser.add_argument("--mode", choices=[mode.value for mode in ExecutionMode], default="normal")
    arguments = parser.parse_args(argv)
    mode = ExecutionMode(arguments.mode)
    try:
        module = load_module(arguments.manifest, mode)
        if arguments.command == "validate":
            result = {
                "module": module.logic.name,
                "version": module.logic.version,
                "semantic_state": module.semantic_state.value,
                "diagnostics": _diagnostics(module.diagnostics),
            }
        else:
            execution = execute(module)
            result = {
                "module": module.logic.name,
                "value": execution.value,
                "variables": execution.variables,
                "diagnostics": _diagnostics(execution.diagnostics),
                "trace": execution.trace,
            }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except DA4LLMError as error:
        diagnostics = getattr(error, "diagnostics", None)
        if diagnostics is None and getattr(error, "diagnostic", None) is not None:
            diagnostics = [error.diagnostic]
        print(json.dumps({
            "status": "error",
            "message": str(error),
            "diagnostics": _diagnostics(diagnostics or ()),
        }, indent=2, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
