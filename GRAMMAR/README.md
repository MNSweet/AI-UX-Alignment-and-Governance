# **Grammar & Opcodes — Execution Language Specification**

The **Grammar** defines the formal language used to express governance rules, execution policies, memory controls, tool boundaries, and state transitions across the Human⥈AI Interoperability Layer. Where HAIL describes *what* must happen, the Grammar and Opcodes define *how* those rules are written, parsed, and enforced.

This directory contains the **complete language specification**:

* The **grammar syntax** (tokens, conditions, rule structure)
* The **example procedures** (e.g., `TASKER_XML_REFERENCE`, `REQUIRE_FILE`)
* The **opcode library** that gives each rule executable semantics
* The **parsing contract** that makes these rules deterministic and machine-first

Together, these components form the *governance engine* that all HAIL-compliant agents must use.

---

## **Purpose of the Grammar**

The Grammar provides a **minimal, deterministic, auditable language** for writing governance logic.
It is intentionally strict:

* **One rule per line**
* **ASCII-only messages**
* **Fixed uppercase identifiers**
* **Explicit control flow**
* **No implicit behavior**

The goal is to eliminate ambiguity.
If a rule fires, it fires predictably.
If it fails, it fails loudly.

This discipline ensures that human intent, safety boundaries, and execution ethics do not degrade under conversational drift or model hallucination.

---

## **Core Concepts**

### **1. GRAMMAR_PARSE**

Defines the structure of the language:

* **TOKENS**:
  `VERB`, `COND`, `MSG`
* **RULE**:
  `IF COND -> VERB [MSG]? ;`
* **BLOCK**:
  A named container with

  * a **PRECONDITION**
  * an **ACTION** section containing ordered rules
  * a **STATE** section describing exposed state variables or outputs

This makes each HAIL component a *formal program* with clear entry conditions and predictable exit states.

---

### **2. Procedures (e.g., TASKER_XML_REFERENCE, REQUIRE_FILE)**

Procedures define **governed behaviors** that must run at specific times—thread start, tool execution, memory saves, etc.

Examples:

* **TASKER_XML_REFERENCE**
  Initiates when mobile automation tool Tasker is referenced. Informed the model of "AUTHORITATIVE_DOCS" that keeps data set accurate to the 

* **REQUIRE_FILE**
  A search-and-bind routine that sequentially queries data sources until it resolves a file reference.
  It tracks:

  * `FILE` (boolean success)
  * `SRC` (the selected file pointer)

These procedures are not suggestions — they are executable governance rules.

---

### **3. Opcodes**

Every rule in a procedure uses an **opcode**, which defines its actual behavior.
The opcode library (in `opcodes.definitions.txt`) includes primitives for:

* **User-facing emission**:
  `EMIT_CHAT`, `EMIT_LOG`, `EMIT_CTX`
* **Flow control**:
  `HALT`, `CONTINUE`, `RETRY`
* **Guard rails**:
  `ASSERT`, `REQUIRE`
* **Dissent / Error**:
  `WARN`, `ERROR`, `DENY`
* **State mutation**:
  `SET`, `CLEAR`, `PUSH_STATE`, `POP_STATE`
* **Tool execution**:
  `CALL_TOOL`
* **Memory operations**:
  `SAVE_BIO`, `SAVE_PROJECT`
* **Domain switching**:
  `SET_DOMAIN`

Each opcode enforces deterministic semantics:
no opcode has hidden behavior, side effects, or inference-based guessing.

---

## **Design Principles**

### **Determinism**

Rules execute top-to-bottom with no stochastic interpretation.
If multiple rules match, all matching rules fire unless a `HALT` or `ERROR` occurs.

### **Auditability**

Every opcode that touches tools, memory, or external state emits audit metadata (UUID, context hash, token ID, etc.).

### **Domain Separation**

Grammar rules explicitly prevent cross-domain operations unless the user intentionally triggers them.
Examples:

* No memory writes without an approval token
* No canvas edits without CTDP gating
* No tool use unless declared in-domain and fully bound

### **Machine-First, Human-Legible**

The grammar is built for parsers first and humans second.
It is readable, but correctness always outweighs convenience.

---

## **File Overview**

```
GRAMMAR/
│
├── grammar.procedure.txt
│     Core grammar rules, token definitions, and syntax structure.
│
├── opcodes.definitions.txt
│     All opcode names, expected arguments, descriptions, and execution semantics.
│
├── HAIL_ENTRY.procedure
│     Boot-time governance sequence loaded at thread initialization.
│
├── REQUIRE_FILE.procedure
│     File search orchestration logic with deterministic fallback ordering.
│
└── (other *.procedure files)
      Additional procedures governing tool use, memory, domain logic, etc.
```

---

## Compact BIO Variant (Streamlined Grammar & Opcodes)

Because full HAIL grammar can be large, a **compact subset** is stored in BIO (global assistant memory) to provide a lightweight bootstrap layer. This BIO-held version preserves most of the functional behavior while minimizing surface area and complexity.

The compact variant:

* Defines a **core bootstrap for grammar library** (`GRAMMAR_PARSE`)
* Defines a **core opcode semantics table** (`OPCODE_SEMANTICS v1.0`)
* Is optimized for **fast loading and deterministic behavior**, not for human editing
* Delegates to the full grammar in this directory when richer behavior is required

### Example: GRAMMAR_PARSE (BIO Compact Form)

```text
#@type:grammar;@schema:bootstrap;
GRAMMAR_PARSE {
TOKENS:
  VERB := EMIT|HALT|CONTINUE|RETRY
  COND := [A-Z0-9_]+ 
  MSG  := "ASCII no emoji"
RULE  := IF COND -> VERB [MSG]? ;
BLOCK := NAME "{" PRECONDITION : COND "\n" ACTION : { RULE } STATE : "{" STATES "}" "\n" "}"
NOTES:
  - ASCII only
  - One RULE per line, end with semicolon
  - Uppercase identifiers <= 20 chars
}
```

This version keeps the entire bootstrap orchestration in a single, tightly scoped to a minimum  required spec that can be interpreted directly from BIO without needing to load the full grammar tree. This record contains the core functions required to important the full library or abstract gracefully any non defined Verbs (OPCODES)

### Example: OPCODE_SEMANTICS (BIO Compact Form)

```text
OPCODE_SEMANTICS v1.0 
OPCODES=EMIT_CHAT,EMIT_LOG,EMIT_CTX,HALT,CONTINUE,RETRY,REQUIRE,ASSERT,WARN,ERROR,DENY,SET,CLEAR,PUSH_STATE,POP_STATE,CALL_TOOL,DELEGATE,SAVE_BIO,SAVE_PROJECT,SET_DOMAIN
EMIT_CHAT: output=user continue
EMIT_LOG: output=log continue
EMIT_CTX: output=context continue
HALT: flow=halt
CONTINUE: flow=next_rule
RETRY: flow=retry engine_guarded
REQUIRE: guard=must_be_true on_fail=log_and_halt
ASSERT: guard=invariant on_fail=halt
WARN: dissent=inline continue
ERROR: dissent=breaking halt
DENY: dissent=fatal halt
SET: state=set_scalar continue
CLEAR: state=delete_scalar continue
PUSH_STATE: state=push continue
POP_STATE: state=pop continue
CALL_TOOL: tool=invoke on_error=ERROR tool_failed
DELEGATE: handoff=record continue
SAVE_BIO: memory=global on_block=DENY bio_blocked
SAVE_PROJECT: memory=project on_block=DENY project_blocked
SET_DOMAIN: domain in {EXECUTION,LOADING} continue
PRECEDENCE: local_grammar > bio_capsule > engine_defaults.
```

This table is the **minimal semantic layer** the assistant needs in BIO to interpret grammar blocks: every opcode has an explicit domain, failure mode, and continuation behavior. When combined with the compact procedures, it enables:

* Deterministic flow control
* Safe tool invocation
* Explicit dissent/error behavior
* Controlled memory operations

The full `GRAMMAR/` directory then extends this compact layer with richer procedures, additional rules, and more detailed governance constructs while remaining compatible with this BIO-stored core.

BIO-stored core is loaded for all assistances. Until over written by the larger library.

---

## **Usage within HAIL as example**

Every HAIL component (DDD, ECE, AVP, CTDP, T2I, MEM, EFD, TTS) ultimately compiles down to:

* **conditions**
* **rules**
* **opcodes**
* **state transitions**

This ensures:

* predictable dissent behavior
* correct sequencing of ethics and verification
* safe execution of tool calls
* traceable memory effects
* context integrity across the entire conversation

HAIL uses this grammar as the **source of truth** for its operational behavior.

---

## **Why This Matters**

LLMs are powerful but nondeterministic.
Grammar provides:

* structure
* boundaries
* explicit decision gates
* reproducible outcomes

Without this, governance systems degrade under ambiguity.
With it, they become inspectable software artifacts.