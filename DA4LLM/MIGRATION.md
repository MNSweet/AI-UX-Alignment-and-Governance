# DA4LLM Migration Map

This document records the initial relationship between preserved repository material and the new DA4LLM packages. It is a migration guide, not approval to copy legacy behavior unchanged.

## Mapping

| Legacy source | Status | DA4LLM destination or use |
| --- | --- | --- |
| `GRAMMAR/` | Legacy; superseded | Selected and adapted model-agnostic material may move into `CORE`. The term grammar remains appropriate only for literal parse grammar or syntax. |
| `HAIL/` | Legacy; superseded | Selected governance, dissent, memory-control, source-authority, and user-control concepts may move into `GOVERNANCE`. |
| `AgentPad/` | Deprecated / EOL | Reference only. Canmore-dependent behavior is not carried forward literally; relevant side-effect lessons may inform BRIDGE or GOVERNANCE review. |
| `CCFT/` | Deprecated / EOL | Reference only. Its GPT/project behavior is slated for deletion and does not map cleanly to Skills. |
| `JobEval/` | Legacy domain package | Retained as a regression and stress-test corpus under `TESTS`; resume scoring and domain rules do not become CORE logic. |
| `Paper2Podcast/` | EOL by developer decision | Reference only unless explicitly revived. |

## Boundary rules

- `CORE` contains no provider invocation instructions, HAIL policy, JobEval scoring, or platform-specific connector behavior.
- `BRIDGE` maps abstract capabilities to concrete providers, tools, connectors, and runtimes.
- `GOVERNANCE` remains a separate layer that can consume CORE diagnostics and traces without changing CORE syntax or parser behavior.
- `TESTS` may preserve legacy examples as fixtures without making their domain assumptions normative.

## Controlled migration process

1. Identify the exact source artifact and candidate behavior.
2. Record the decision in the selection ledger as adopt, adapt, defer, or reject.
3. Assign the destination package and document conflicts or overrides.
4. Define the test requirement and package-boundary check.
5. Promote only reviewed material; preserve source provenance.

No legacy file is removed, renamed, or overwritten by this bootstrap migration.
