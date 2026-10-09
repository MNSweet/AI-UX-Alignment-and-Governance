# AI UX, Alignment, and Governance

This repository preserves the development lineage of several AI interaction, alignment, and governance frameworks. DA4LLM stands for **D**eterministic **A**rchitecture for **L**arge **L**anguage **M**odels and is the current active architecture.

## Current architecture

### [DA4LLM](DA4LLM/README.md)

DA4LLM separates deterministic behavior into three packages:

- **CORE**: provider-neutral syntax, control, operations, primitives, procedures, semantics, state, trace, diagnostics, and abstract capability contracts.
- **BRIDGE**: provider-, tool-, connector-, and runtime-specific mappings and missing-capability behavior.
- **GOVERNANCE**: HAIL-derived governance, dissent, memory control, source authority, user-control rules, and parity-share protocols.

The repository currently contains the DA4LLM topology and project documentation only. Candidate logic remains subject to the selection ledger and has not been migrated by this bootstrap change.

## Legacy and reference material

Legacy content remains in place for provenance, migration review, and regression testing. It is not the current architecture unless explicitly revived or promoted through the DA4LLM process.

| Directory | Status | DA4LLM relationship |
| --- | --- | --- |
| [`GRAMMAR/`](GRAMMAR/README.md) | Legacy; superseded | Source material for `DA4LLM/CORE`, subject to selection and adaptation. |
| [`HAIL/`](HAIL/README.md) | Legacy; superseded | Governance lineage for `DA4LLM/GOVERNANCE`. |
| [`AgentPad/`](AgentPad/README.md) | Deprecated / EOL | Preserved as reference; depended on the deprecated Canmore surface. |
| [`CCFT/`](CCFT/README.md) | Deprecated / EOL | Preserved as reference; its GPT/project model is slated for deletion and does not map cleanly to Skills. |
| [`JobEval/`](JobEval/README.md) | DA4LLM domain application | Runs on DA4LLM; it is not a predecessor to DA4LLM or part of CORE. |
| [`Paper2Podcast/`](Paper2Podcast/README.md) | EOL by developer decision | Preserved as reference unless explicitly revived. |

No legacy directory has been removed, renamed, or rewritten as part of the DA4LLM bootstrap.

## Migration status

See [`DA4LLM/STATUS.md`](DA4LLM/STATUS.md) for current scope and [`DA4LLM/MIGRATION.md`](DA4LLM/MIGRATION.md) for package boundaries and legacy mappings.
