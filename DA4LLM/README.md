# DA4LLM

DA4LLM (Deterministic Architecture for Large Language Models) is the current active architecture in this repository. It is being constructed alongside the preserved legacy systems so that provenance, migration decisions, and regression evidence remain reviewable.

## Architecture

| Package | Responsibility |
| --- | --- |
| [`CORE/`](CORE/README.md) | Model-agnostic deterministic syntax, control, operations, primitives, procedures, semantics, state, trace, diagnostics, and abstract capability contracts. |
| [`BRIDGE/`](BRIDGE/README.md) | Provider-, tool-, connector-, and runtime-specific mappings, substitutions, and missing-capability behavior. |
| [`GOVERNANCE/`](GOVERNANCE/README.md) | HAIL-derived governance, dissent, memory control, source authority, user-control rules, and parity-share protocols. |
| [`TESTS/`](TESTS/README.md) | Conformance fixtures, boundary tests, golden traces, and legacy regression cases. |
| [`docs/`](docs/README.md) | Roadmap, terminology, design decisions, and supporting migration documentation. |

## Current scope

This bootstrap establishes repository topology and truthful project documentation. It does not migrate the full harness, promote candidate specifications, or rewrite legacy content.

The Google Drive DA4LLM workspace remains the staging and audit context for source selection. Promotion into DA4LLM requires a recorded source, destination package, decision, rationale, conflict or override note, and test requirement. Candidate and staging documents are not authoritative specifications merely because they are referenced here.

## Package order

Development proceeds in this order:

1. Stabilize the small, provider-neutral `CORE`.
2. Add concrete provider and runtime mappings in `BRIDGE`.
3. Attach the separate `GOVERNANCE` layer without changing CORE parsing or control semantics.

See [STATUS.md](STATUS.md) for the present state and [MIGRATION.md](MIGRATION.md) for legacy mappings.
