"""Shared data structures for the DA4LLM CORE proof of concept."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol


class ExecutionMode(str, Enum):
    NORMAL = "normal"
    DEBUG = "debug"
    STRICT = "strict"


class SemanticState(str, Enum):
    COMPLETE = "SEMANTIC_COMPLETE"
    PARTIAL = "SEMANTIC_PARTIAL"
    ABSENT = "SEMANTIC_ABSENT"


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str
    severity: str = "warning"
    line: int | None = None


@dataclass(frozen=True)
class Literal:
    raw: str
    value: Any
    lexical_type: str
    line: int


@dataclass(frozen=True)
class SetStatement:
    name: str
    value: Literal
    line: int
    opcode: str = field(default="SET", init=False)


@dataclass(frozen=True)
class CapabilityStatement:
    capability: str
    payload_variable: str | None
    result_variable: str | None
    on_unavailable: str
    line: int
    opcode: str = field(default="CALL_CAPABILITY", init=False)


@dataclass(frozen=True)
class ReturnStatement:
    variable: str
    line: int
    opcode: str = field(default="RETURN", init=False)


Statement = SetStatement | CapabilityStatement | ReturnStatement


@dataclass(frozen=True)
class LogicModule:
    name: str
    version: str
    procedure: str
    statements: tuple[Statement, ...]
    source: Path


@dataclass(frozen=True)
class SemanticContract:
    module: str
    module_version: str
    variables: dict[str, dict[str, Any]]
    operations: dict[str, dict[str, Any]]
    source: Path


@dataclass(frozen=True)
class ModuleManifest:
    module: str
    module_version: str
    logic_path: Path
    semantic_path: Path | None
    source: Path


@dataclass(frozen=True)
class ValidatedModule:
    manifest: ModuleManifest
    logic: LogicModule
    semantics: SemanticContract | None
    semantic_state: SemanticState
    diagnostics: tuple[Diagnostic, ...]


@dataclass(frozen=True)
class CapabilityResult:
    status: str
    capability: str
    value: Any = None
    diagnostic: Diagnostic | None = None


@dataclass(frozen=True)
class ExecutionResult:
    value: Any
    variables: dict[str, Any]
    diagnostics: tuple[Diagnostic, ...]
    trace: tuple[str, ...]


class CapabilityBridge(Protocol):
    """Provider-neutral interface implemented by a future BRIDGE package."""

    def call(self, capability: str, payload: Any) -> Any:
        """Invoke a generic capability or raise CapabilityUnavailable."""


class GovernanceHooks(Protocol):
    """Optional lifecycle interface implemented by GOVERNANCE modules."""

    def apply(self, hook: str, context: dict[str, Any]) -> None:
        """Observe or constrain a declared lifecycle hook."""


class DA4LLMError(Exception):
    """Base class for deterministic CORE failures."""


class LexError(DA4LLMError):
    pass


class ParseError(DA4LLMError):
    pass


class ValidationError(DA4LLMError):
    def __init__(self, diagnostics: list[Diagnostic] | tuple[Diagnostic, ...]):
        self.diagnostics = tuple(diagnostics)
        super().__init__("; ".join(item.message for item in self.diagnostics))


class ExecutionError(DA4LLMError):
    def __init__(self, diagnostic: Diagnostic):
        self.diagnostic = diagnostic
        super().__init__(diagnostic.message)


class CapabilityUnavailable(DA4LLMError):
    pass
