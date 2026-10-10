# DA4LLM Status

## Current phase

**Executable CORE proof of concept / pre-release-candidate review**

DA4LLM remains the active architecture. CORE now has a minimal executable validator and interpreter; BRIDGE and GOVERNANCE remain explicit placeholders.

## Included in this phase

- Minimal lexer, parser, semantic loader, validator, and procedure runtime.
- `normal`, `debug`, and `strict` validation modes.
- Canonical POC operations: `SET`, `CALL_CAPABILITY`, and `RETURN`.
- Typed `CAPABILITY_UNAVAILABLE` handling controlled by the calling procedure.
- Optional GOVERNANCE lifecycle hook declarations.
- Executable conformance tests and a standalone example.
- BRIDGE and GOVERNANCE placeholders that make no implementation claims.

## Not included in this phase

- Full harness or legacy parser migration.
- Promotion of candidate CORE files into authoritative specifications.
- Provider-specific bridge implementations.
- HAIL, Parity Share, DDD, or other governance-policy implementation.
- JobEval logic, data, weighting, resumes, or domain-specific behavior.
- Rewriting, moving, renaming, or deleting legacy artifacts.
- Stable syntax, schema, runtime, versioning, or output-contract decisions.

## Promotion gate

The POC code is a normalized candidate implementation. It does not promote the reviewed historical files wholesale. A future release candidate still requires recorded source, destination package, decision, rationale, conflict or override note, and test requirement.

## Next controlled phase

Review the POC language, semantic contract, and validator behavior. Stabilize CORE only after those decisions are accepted. Concrete BRIDGE mappings and reviewed GOVERNANCE modules follow separately.
