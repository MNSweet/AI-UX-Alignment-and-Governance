# DA4LLM Status

## Current phase

**Language-native CORE candidate / pre-release review**

DA4LLM remains the active architecture. The repository now contains a first model-readable CORE candidate expressed in DA4LLM's own paired logic and semantic files.

## Included in this phase

- CORE bootstrap and explicit interpretation order.
- Lexer and parser logic with paired semantic contracts.
- General procedures, validator, execution modes, and semantic precedence.
- Canonical opcode meanings and primitive procedures.
- Generic `CALL_CAPABILITY` and deterministic `CAPABILITY_UNAVAILABLE` behavior.
- Optional GOVERNANCE lifecycle hooks.
- Paired nonimplementation placeholders for BRIDGE and GOVERNANCE.
- Language-native conformance fixtures.

## Not included in this phase

- Promotion of candidate CORE files into an authoritative release.
- Provider-specific bridge implementations.
- HAIL, Parity Share, DDD, or other governance-policy implementations.
- Domain-application logic, data, weighting, personal information, or domain behavior.
- A host-language interpreter or required software runtime.
- Rewriting, moving, renaming, or deleting legacy artifacts.
- Final syntax, versioning, coercion, capability registry, or output-contract decisions.

## Promotion gate

The candidate files normalize approved architecture and reviewed source lineage without promoting legacy material wholesale. A stable release still requires selection-ledger decisions, rationale, conflict or override notes, and conformance requirements.

## Next controlled phase

Review the candidate lexer, parser, opcode registry, primitive behavior, semantic contracts, and conformance traces. BRIDGE mappings and GOVERNANCE modules follow as separate reviewed changes.
