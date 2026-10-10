# DA4LLM

DA4LLM stands for **D**eterministic **A**rchitecture for **L**arge **L**anguage **M**odels. It is the current active architecture in this repository and is being constructed alongside preserved legacy systems so that provenance and migration decisions remain reviewable.

## Architecture

| Package | Responsibility |
| --- | --- |
| [`CORE/`](CORE/README.md) | Model-agnostic deterministic syntax, control, operations, primitives, procedures, semantics, state, trace, diagnostics, and abstract capability contracts. |
| [`BRIDGE/`](BRIDGE/README.md) | Provider-, tool-, connector-, and runtime-specific mappings, substitutions, and missing-capability behavior. |
| [`GOVERNANCE/`](GOVERNANCE/README.md) | HAIL-derived governance, dissent, memory control, source authority, user-control rules, and parity-share protocols. |
| [`TESTS/`](TESTS/README.md) | Conformance fixtures, boundary tests, golden traces, and legacy regression cases. |
| [`docs/`](docs/README.md) | Roadmap, terminology, design decisions, and supporting migration documentation. |

## Current scope

The repository contains the first language-native DA4LLM CORE candidate. DA4LLM is a prompt-native, in-context language: its files enter a model's active context through project files, prompt attachments, or an equivalent context-loading mechanism, and the model interprets the declared lexer, parser, procedures, opcodes, and semantics.

DA4LLM is not implemented in a host programming language. Conventional software may later provide optional authoring or conformance tools, but such tooling is not CORE and is not required to interpret DA4LLM.

The current files are reviewable `0.1.0-candidate` artifacts, not a stable release. BRIDGE and GOVERNANCE remain paired placeholders with no provider mapping or policy implementation.

The Google Drive DA4LLM workspace remains the staging and audit context for source selection. Promotion into DA4LLM requires a recorded source, destination package, decision, rationale, conflict or override note, and test requirement. Candidate and staging documents are not authoritative specifications merely because they are referenced here.

## Package order

Development proceeds in this order:

1. Review and stabilize the small, model-readable `CORE` language candidate.
2. Add concrete provider and runtime mappings in `BRIDGE`.
3. Attach the separate `GOVERNANCE` layer without changing CORE parsing or control semantics.

See [STATUS.md](STATUS.md) for the present state and [MIGRATION.md](MIGRATION.md) for legacy mappings.
