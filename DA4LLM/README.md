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

The repository contains a deliberately small, executable CORE proof of concept. It validates the approved separation between logic and semantics, supports three validation modes, runs without BRIDGE or GOVERNANCE, and exposes provider-neutral capability and governance extension boundaries.

This is not a production release or a complete migration of the legacy harness. The syntax, file formats, and `0.1.0-poc` version label remain provisional. BRIDGE and GOVERNANCE contain honest placeholders only; no provider mapping or governance policy is represented as implemented.

The Google Drive DA4LLM workspace remains the staging and audit context for source selection. Promotion into DA4LLM requires a recorded source, destination package, decision, rationale, conflict or override note, and test requirement. Candidate and staging documents are not authoritative specifications merely because they are referenced here.

## Package order

Development proceeds in this order:

1. Review and stabilize the small, provider-neutral `CORE` proof of concept.
2. Add concrete provider and runtime mappings in `BRIDGE`.
3. Attach the separate `GOVERNANCE` layer without changing CORE parsing or control semantics.

See [STATUS.md](STATUS.md) for the present state and [MIGRATION.md](MIGRATION.md) for legacy mappings.
