# DA4LLM CORE

CORE is the small, model-agnostic deterministic kernel. This directory now contains an executable proof of concept for syntax, parsing, procedure execution, semantic resolution, diagnostics, provider-neutral capability contracts, and declared extension hooks.

The proof of concept is review material, not a stable specification. Its syntax, JSON shapes, Python runtime, and `0.1.0-poc` version are provisional.

## Structure

| Area | POC responsibility |
| --- | --- |
| `LOGIC/LEXER/` | Convert source text into tokens with deterministic lexical defaults. |
| `LOGIC/PARSER/` | Parse a small procedure language without provider or policy knowledge. |
| `LOGIC/PROCEDURES/` | Execute canonical operations in declared order. |
| `SEMANTICS/` | Load declarative meaning, type, purpose, and intrinsic restrictions. |
| `SEMANTICS/OPERATIONS/` | Declare the current canonical POC opcodes. |
| `CAPABILITIES/` | Define and invoke the generic BRIDGE-facing capability contract. |
| `EXTENSION_HOOKS/` | Declare optional GOVERNANCE lifecycle hooks. |

Semantics may constrain interpretation but may not contain procedural control flow. For literal values, an explicit semantic type takes precedence over the lexical default. If no semantic type is present, CORE uses deterministic lexical defaults: `"4"` is a string, `4` is an integer, `4.0` is a float, `TRUE` is a boolean, and `NULL` is null.

## Execution modes

| Mode | Behavior |
| --- | --- |
| `normal` | Run with deterministic defaults and suppress nonessential missing-semantics warnings. |
| `debug` | Run identically to normal mode while exposing missing, partial, and unused semantic definitions. |
| `strict` | Require a complete compatible semantic contract before execution. |

Execution-critical errors, including undefined variables and incompatible declared types, fail in every mode. CORE does not silently ask a model to guess an execution-critical meaning.

## Current POC language

The deliberately narrow language supports `SET`, `CALL_CAPABILITY`, and `RETURN` inside one procedure. A caller declares whether a missing capability should `CONTINUE` or `HALT`. CORE never names or selects an ecosystem-specific tool.

The example under `examples/standalone/` requests a generic capability without a BRIDGE. It continues with a typed `CAPABILITY_UNAVAILABLE` diagnostic and returns its local value, proving that CORE remains independently executable.

The POC uses only the Python standard library and requires Python 3.10 or newer. From the repository root:

```sh
python3 -m DA4LLM.CORE.cli validate DA4LLM/CORE/examples/standalone/manifest.json --mode strict
python3 -m DA4LLM.CORE.cli run DA4LLM/CORE/examples/standalone/manifest.json --mode normal
python3 -m unittest discover -s DA4LLM/TESTS -v
```

See [`../docs/POC_PROVENANCE.md`](../docs/POC_PROVENANCE.md) for source and exclusion boundaries.
