from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from DA4LLM.CORE.LOGIC.LEXER import TokenKind, tokenize
from DA4LLM.CORE.LOGIC.PROCEDURES import execute
from DA4LLM.CORE.model import (
    CapabilityUnavailable,
    ExecutionError,
    ExecutionMode,
    SemanticState,
    ValidationError,
)
from DA4LLM.CORE.validator import load_module


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "CORE" / "examples" / "standalone" / "manifest.json"


class CorePOCTests(unittest.TestCase):
    def _module(self, logic: str, semantics: dict | None, mode=ExecutionMode.NORMAL):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        folder = Path(temp.name)
        (folder / "module.logic.da4").write_text(logic, encoding="utf-8")
        manifest = {
            "module": "test_module",
            "module_version": "0.1.0-poc",
            "logic": "module.logic.da4",
        }
        if semantics is not None:
            (folder / "module.semantic.json").write_text(json.dumps(semantics), encoding="utf-8")
            manifest["semantics"] = "module.semantic.json"
        (folder / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        return load_module(folder / "manifest.json", mode)

    @staticmethod
    def _logic(body: str) -> str:
        return (
            'MODULE test_module VERSION "0.1.0-poc"\n'
            "PROCEDURE main\n"
            f"{body}\n"
            "END\n"
        )

    @staticmethod
    def _semantics(variables=None, operations=None):
        return {
            "module": "test_module",
            "module_version": "0.1.0-poc",
            "variables": variables or {},
            "operations": operations or {},
        }

    def test_lexer_assigns_deterministic_literal_types(self):
        tokens = tokenize('"4" 4 4.0 TRUE NULL\n')
        kinds = [token.kind for token in tokens if token.kind not in {TokenKind.NEWLINE, TokenKind.EOF}]
        self.assertEqual(kinds, [
            TokenKind.STRING, TokenKind.INTEGER, TokenKind.FLOAT, TokenKind.BOOLEAN, TokenKind.NULL
        ])

    def test_complete_example_uses_semantics_before_lexical_default(self):
        module = load_module(EXAMPLE, ExecutionMode.STRICT)
        result = execute(module)
        self.assertEqual(module.semantic_state, SemanticState.COMPLETE)
        self.assertEqual(result.value, "4")
        self.assertIsInstance(result.value, str)

    def test_normal_mode_suppresses_absent_semantics_warning(self):
        module = self._module(self._logic("SET value = 4\nRETURN value"), None)
        self.assertEqual(module.semantic_state, SemanticState.ABSENT)
        self.assertEqual(module.diagnostics, ())
        self.assertEqual(execute(module).value, 4)

    def test_debug_mode_reports_absent_semantics(self):
        module = self._module(
            self._logic("SET value = 4\nRETURN value"), None, ExecutionMode.DEBUG
        )
        self.assertEqual(module.diagnostics[0].code, "SEMANTIC_ABSENT")

    def test_strict_mode_rejects_absent_semantics(self):
        with self.assertRaises(ValidationError) as caught:
            self._module(self._logic("SET value = 4\nRETURN value"), None, ExecutionMode.STRICT)
        self.assertIn("SEMANTIC_REQUIRED", [item.code for item in caught.exception.diagnostics])

    def test_partial_semantics_are_visible_in_debug(self):
        module = self._module(
            self._logic("SET value = 4\nRETURN value"),
            self._semantics(
                variables={"value": {"type": "integer", "purpose": "Test value"}},
                operations={"SET": {"meaning": "Assign"}},
            ),
            ExecutionMode.DEBUG,
        )
        self.assertEqual(module.semantic_state, SemanticState.PARTIAL)
        self.assertIn("SEMANTIC_PARTIAL", [item.code for item in module.diagnostics])

    def test_semantics_may_not_contain_control_flow(self):
        with self.assertRaises(ValidationError) as caught:
            self._module(
                self._logic("SET value = 4\nRETURN value"),
                self._semantics(
                    variables={"value": {"type": "integer", "purpose": "Test value"}},
                    operations={
                        "SET": {"meaning": "Assign", "if": "forbidden"},
                        "RETURN": {"meaning": "Return"},
                    },
                ),
            )
        self.assertIn("SEMANTIC_CONTAINS_LOGIC", [item.code for item in caught.exception.diagnostics])

    def test_declared_type_mismatch_fails_validation_in_every_mode(self):
        with self.assertRaises(ValidationError) as caught:
            self._module(
                self._logic('SET value = "not-a-number"\nRETURN value'),
                self._semantics(
                    variables={"value": {"type": "integer", "purpose": "Test value"}},
                    operations={
                        "SET": {"meaning": "Assign"},
                        "RETURN": {"meaning": "Return"},
                    },
                ),
            )
        self.assertIn("SEMANTIC_TYPE_MISMATCH", [item.code for item in caught.exception.diagnostics])

    def test_strict_mode_rejects_semantics_without_required_purpose(self):
        with self.assertRaises(ValidationError) as caught:
            self._module(
                self._logic("SET value = 4\nRETURN value"),
                self._semantics(
                    variables={"value": {"type": "integer"}},
                    operations={
                        "SET": {"meaning": "Assign"},
                        "RETURN": {"meaning": "Return"},
                    },
                ),
                ExecutionMode.STRICT,
            )
        self.assertIn("SEMANTIC_REQUIRED", [item.code for item in caught.exception.diagnostics])

    def test_manifest_references_cannot_escape_module_directory(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        folder = Path(temp.name)
        manifest = {
            "module": "test_module",
            "module_version": "0.1.0-poc",
            "logic": "../outside.logic.da4",
        }
        (folder / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(ValidationError) as caught:
            load_module(folder / "manifest.json")
        self.assertIn("MANIFEST_PATH_OUTSIDE_MODULE", [item.code for item in caught.exception.diagnostics])

    def test_missing_bridge_can_continue_with_typed_diagnostic(self):
        module = load_module(EXAMPLE, ExecutionMode.NORMAL)
        result = execute(module)
        self.assertIn("CAPABILITY_UNAVAILABLE", [item.code for item in result.diagnostics])
        self.assertEqual(result.value, "4")

    def test_missing_bridge_can_halt_when_caller_requires_it(self):
        module = self._module(
            self._logic(
                'SET payload = "hello"\n'
                'CALL_CAPABILITY "text.echo" WITH payload ON_UNAVAILABLE HALT\n'
                "RETURN payload"
            ),
            None,
        )
        with self.assertRaises(ExecutionError) as caught:
            execute(module)
        self.assertEqual(caught.exception.diagnostic.code, "CAPABILITY_UNAVAILABLE")

    def test_bridge_implementation_remains_provider_neutral_to_core(self):
        class Bridge:
            def call(self, capability, payload):
                if capability != "text.echo":
                    raise CapabilityUnavailable(capability)
                return payload.upper()

        module = self._module(
            self._logic(
                'SET payload = "hello"\n'
                'CALL_CAPABILITY "text.echo" WITH payload AS result\n'
                "RETURN result"
            ),
            None,
        )
        self.assertEqual(execute(module, bridge=Bridge()).value, "HELLO")

    def test_governance_receives_only_declared_hooks(self):
        class Governance:
            def __init__(self):
                self.hooks = []

            def apply(self, hook, context):
                self.hooks.append(hook)

        governance = Governance()
        module = load_module(EXAMPLE, ExecutionMode.NORMAL)
        execute(module, governance=governance)
        self.assertEqual(governance.hooks, [
            "PRE_EXECUTION", "PRE_CAPABILITY", "POST_CAPABILITY", "PRE_OUTPUT", "POST_OUTPUT"
        ])


if __name__ == "__main__":
    unittest.main()
