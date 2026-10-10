# DA4LLM CORE

CORE is the small, model-agnostic language kernel. It defines how DA4LLM source is recognized, structured, interpreted, validated, and applied inside an LLM context.

The model is the interpreter. CORE is therefore expressed as paired DA4LLM logic and semantic files rather than as code in a pre-existing programming language.

## Candidate modules

| Pair | Responsibility |
| --- | --- |
| `CORE_BOOTSTRAP.*.da4llm` | Required module inventory, load order, optional-layer boundary, and readiness state. |
| `LOGIC/LEXER/LEXER.*.da4llm` | Token recognition and lexical defaults. |
| `LOGIC/PARSER/PARSER.*.da4llm` | Logic blocks, semantic blocks, action rules, state sections, and parse failures. |
| `LOGIC/PROCEDURES/PROCEDURES.*.da4llm` | Request execution, top-to-bottom rule evaluation, dispatch, and domain-neutral utilities. |
| `LOGIC/PROCEDURES/VALIDATOR.*.da4llm` | Module pairing, execution modes, semantic coverage, version checks, and value resolution. |
| `SEMANTICS/OPERATIONS/OPCODES.*.da4llm` | Canonical operation resolution and declarative opcode meanings. |
| `SEMANTICS/OPERATIONS/PRIMITIVE_PROCEDURES/PRIMITIVES.*.da4llm` | Reserved model-readable primitive procedures and their contracts. |
| `CAPABILITIES/CALL_CAPABILITY.*.da4llm` | Provider-neutral external capability request and missing-BRIDGE behavior. |
| `EXTENSION_HOOKS/EXTENSION_HOOKS.*.da4llm` | Optional GOVERNANCE attachment points and extension limits. |

Each executable module has a logic file and a semantic file with an exact shared module name and version. Logic declares ordering, conditions, operations, and state transitions. Semantics declares type, purpose, meaning, defaults, and intrinsic restrictions; it cannot contain procedural control flow.

## Interpretation order

1. Lexer logic and semantics.
2. Parser logic and semantics.
3. Opcode logic and semantics.
4. Primitive procedure logic and semantics.
5. General procedure logic and semantics.
6. Generic capability logic and semantics.
7. Extension-hook logic and semantics.
8. Validator logic and semantics.
9. Optional BRIDGE, then optional GOVERNANCE.

CORE must validate and operate without BRIDGE or GOVERNANCE. Calling an unavailable external capability returns `CAPABILITY_UNAVAILABLE`; the calling procedure declares whether that result continues or halts execution. Missing GOVERNANCE is a no-op unless the request explicitly requires it.

## Execution modes

| Mode | Missing or partial noncritical semantics |
| --- | --- |
| `NORMAL` | Continue using deterministic lexical defaults; suppress the warning. |
| `DEBUG` | Continue with the same behavior and expose the warning. |
| `STRICT` | Emit `SEMANTIC_REQUIRED` and halt. |

Execution-critical ambiguity, unknown opcodes, unresolved variables, incompatible types, and parse failures halt in every mode. Model inference is not permitted to fill an execution-critical gap.

These files are `0.1.0-candidate` review artifacts. They are not yet an authoritative DA4LLM release.
