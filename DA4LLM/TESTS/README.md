# DA4LLM TESTS

TESTS contains model-evaluated DA4LLM conformance fixtures. The fixtures enter context alongside CORE and are interpreted through the same lexer, parser, procedures, opcodes, and semantics being tested.

`CORE_POC.logic.da4llm` and `CORE_POC.semantic.da4llm` cover:

- standalone CORE validation with neither BRIDGE nor GOVERNANCE;
- semantic type precedence over lexical defaults;
- `NORMAL`, `DEBUG`, and `STRICT` incomplete-semantic behavior;
- missing-BRIDGE continue and halt paths;
- absent-GOVERNANCE no-op behavior; and
- rejection of procedural control flow inside semantic entries.

`MINIMUM_POC.prompt.txt` is a portable demonstration prompt for a project or conversation where the candidate files have been made available as context. It requires honest missing-file reporting and returns only conformance state, trace, and diagnostics.

`EXPECT=HALT_EXPECTED` cases pass only when interpretation stops with the named diagnostic. The expectation is test metadata, not an instruction to continue after `HALT`.

These fixtures do not depend on a host-language test runner. Optional external conformance tooling may be added later without becoming part of CORE. Test registration does not promote domain logic into CORE.
