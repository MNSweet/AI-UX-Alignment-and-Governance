# DA4LLM Status

## Current phase

**Bootstrap structure / pre-release-candidate documentation**

This repository now identifies DA4LLM as the active architecture and provides package boundaries for CORE, BRIDGE, GOVERNANCE, TESTS, and supporting documentation.

## Included in this phase

- DA4LLM directory topology and entrypoint documentation.
- CORE, BRIDGE, GOVERNANCE, and TESTS responsibility boundaries.
- Migration mapping for preserved legacy projects.
- Deprecation and legacy notices that do not alter historical contents.

## Not included in this phase

- Full harness or parser migration.
- Promotion of candidate CORE files into authoritative specifications.
- Provider-specific bridge implementations.
- Rewriting, moving, renaming, or deleting legacy artifacts.
- Resolution of open operation, syntax, capability, versioning, or output-contract decisions.

## Promotion gate

An artifact is not promoted into a DA4LLM release candidate until the selection ledger records its source, destination package, decision, rationale, conflict or override note, and test requirement. Candidate notes remain review material until that gate is satisfied and approved.

## Next controlled phase

Review the selected CORE candidates and resolve their open decisions before adding stable top-level CORE files. BRIDGE and GOVERNANCE implementation follows CORE stabilization.
