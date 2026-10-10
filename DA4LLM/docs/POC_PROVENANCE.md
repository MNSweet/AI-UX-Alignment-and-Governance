# CORE POC Provenance and Exclusions

## Status

The executable files in this proof of concept are newly normalized DA4LLM candidate code. They demonstrate approved architectural boundaries; they are not a verbatim migration or a declaration that a historical file is now authoritative.

## Design lineage reviewed

The POC was informed by the architecture discussions and by review of these supplied historical or candidate artifacts:

- `GRAMMAR.bootstrap.txt`
- `OPCODES.bootstrap.txt`
- `PROCEDURES.grammar.txt`
- `Bridge4CallTool.procedure.txt`
- `HAIL.procedure.txt`
- `REQUIRE_FILE.procedure.txt`
- `hail_latest.grammar.txt`

These artifacts remain preserved in their original locations. Provider-specific calls, mandatory HAIL loading, obsolete platform behavior, and conflicting historical comments were not copied into the POC.

## Approved boundaries represented

- CORE is independently executable and contains logic, semantics, canonical operations, generic capability contracts, and declared extension hooks.
- BRIDGE maps generic capabilities to individual ecosystems but is not required for local CORE execution.
- GOVERNANCE supplies optional alignment-rich context and constraints through declared hooks without rewriting CORE language semantics.
- Every future executable module is expected to pair logic with semantics and a version-matched manifest.
- Missing noncritical semantics may be silent in normal mode, visible in debug mode, and rejected in strict mode. Execution-critical ambiguity is never silently guessed.

## Explicit exclusions

- JobEval is deferred and is not a predecessor or source of CORE logic.
- No JobEval files, resumes, personal data, weighting, or domain rules are included.
- No provider-specific BRIDGE implementation is included.
- No HAIL, Parity Share, DDD, or other GOVERNANCE policy is promoted.
- No legacy file is edited, moved, renamed, or deleted by this POC.

## Provisional decisions

The Python standard-library runtime, `.logic.da4` syntax, JSON semantic and manifest shapes, coercion table, and `0.1.0-poc` label are all provisional. They exist to make the architecture testable and reviewable before stable specification decisions are made.
