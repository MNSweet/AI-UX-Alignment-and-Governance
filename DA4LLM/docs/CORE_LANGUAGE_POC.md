# DA4LLM CORE Language Candidate

## Interpretation model

DA4LLM is a prompt-native, in-context language designed around how a large language model receives context, recognizes structure, resolves meaning, follows ordered procedures, calls available capabilities, and incorporates optional governance.

DA4LLM source becomes part of the model's active environment through project files, prompt attachments, retrieval, or an equivalent context-loading mechanism. The model interprets the language. DA4LLM is not a host-language software project.

The word **execution** in CORE means that the model applies validated DA4LLM logic and semantics during inference. It does not imply a conventional software runtime. External validators or editors may eventually help authors, but they remain optional tooling outside CORE.

## Source lineage

This candidate was newly normalized after reviewing these supplied historical or candidate artifacts:

- `GRAMMAR.bootstrap.txt`
- `OPCODES.bootstrap.txt`
- `PROCEDURES.grammar.txt`
- `Bridge4CallTool.procedure.txt`
- `HAIL.procedure.txt`
- `REQUIRE_FILE.procedure.txt`
- `hail_latest.grammar.txt`

The source artifacts remain unchanged. Their presence informed syntax lineage, procedure style, conflict identification, and package boundaries; no historical artifact is promoted wholesale.

## Deliberate adaptations

- `CALL_TOOL` becomes provider-neutral `CALL_CAPABILITY` in CORE. Concrete tool names belong in BRIDGE.
- Mandatory HAIL loading is not carried forward. GOVERNANCE is optional unless a request explicitly requires it.
- Logic and semantics are paired but separate. Semantic files cannot contain control flow.
- Exact module-version matching replaces the historical HAIL week-code schema for this candidate.
- Execution modes formalize missing-semantic behavior without allowing execution-critical model guessing.
- Comments remain forbidden inside DA4LLM modules; the `#@` first line is a required metadata directive, not a comment.
- Unicode source is permitted, while control characters and multiline string literals remain restricted.
- Canonical names expand from the legacy twenty-character ceiling to forty-eight characters so semantic and diagnostic identifiers remain readable without abbreviation collisions.

## Explicit exclusions

- Domain applications are not CORE lineage. No domain logic, application data, weighting, personal information, or private source material is included.
- Historical provider calls, Canmore behavior, BIO memory calls, and obsolete connector syntax are not included.
- No HAIL, Parity Share, DDD, or other GOVERNANCE policy is promoted in the placeholder.
- No existing legacy file is rewritten, moved, renamed, or deleted.

## Candidate status

Version `0.1.0-candidate` exists to make the language inspectable through concrete paired files and conformance cases. It does not freeze the syntax or certify deterministic behavior across every model ecosystem. Promotion requires user review and recorded selection decisions.

The following procedure references are intentional boundaries rather than missing CORE implementations:

- `BRIDGE_RESOLVE_CAPABILITY` and `BRIDGE_INVOKE_CAPABILITY` belong to a future concrete BRIDGE.
- `GOVERNANCE_HANDLE_HOOK` belongs to a future reviewed GOVERNANCE module.
- `TARGET_PROCEDURE` and `TARGET_PRIMITIVE` are resolved names, not literal procedure identifiers.

The candidate uses a controlled derived-predicate vocabulary so conditions such as `MODULE_SEMANTIC_MISSING` inherit meaning from a declared base rather than requiring duplicate semantic prose. An undeclared base or unknown suffix remains unresolved.
