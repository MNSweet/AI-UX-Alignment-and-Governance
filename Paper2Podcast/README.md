# Paper-to-Podcast Protocol (v1.7)

> **EOL by developer decision:** This project is preserved as legacy reference material and is not part of the active DA4LLM architecture. It may be reconsidered only if explicitly revived.

A formal spec for converting technical papers and posts into long, TTS-friendly podcast monologues that preserve substance, inject clear analysis, and avoid hype.

> TL;DR: Feed it PDFs, docs, or repos; get one continuous spoken monologue that keeps 85–100% of the signal, expands figures and tables into words, and ends with a compact “Sources:” line.

---

## Aquire Protocol
**Download or Copy/Paste**
> JSON Protocol: [Paper2Podcast](Paper2Podcast.json "A premade default one-line drop in ready for the first message of a thread or project instructions")

**Make it your own**
> Customize: [Choose your own Config Settings](Paper2Podcast.html "A wizard that will generate the protocol based on your preferences like Host Personality, Source-Type Whitelist, etc")

---

## Goals

* **High-fidelity transformation:** Preserve at least 85% of the source’s substantive content.
* **Critical clarity:** Explain methods, results, and assumptions in plain language; call out overclaims; separate author claims, paper facts, and inference.
* **Audio-safe output:** Produce a continuous, narrator-ready script with no headings, lists, or formatting that breaks TTS.
* **Evidence accountability:** Attach one “Sources:” line naming the artifacts the narration relied on.
* **Scalable structure:** Use modular segments selected dynamically based on the material.

---

## What it does

The protocol ingests research artifacts and emits a single monologue plus a compact sources line.

* **Inputs (any combination):** PDFs or abstracts, official repos/docs, figures/tables, leaderboards, and release notes.
* **Transformations:**

  * Converts tables, charts, and equations into spoken descriptions.
  * Threads method mechanics, ablations, and benchmarks into narrative.
  * Inserts brief sidebars to examine prescriptive or absolute claims.
* **Outputs:**

  * **Monologue:** one continuous paragraph stream in plain text, TTS-safe.
  * **Sources:** a single trailing line beginning with `Sources:` listing items in terse natural language.

---

## Audience

Technical listeners who want pragmatic explanations and measured critique, not marketing.

---

## Output contract

* **Form:** One continuous monologue. No headings. No lists. No code fences.
* **Coverage:** ≥ 85% of the source’s substantive content. For long sources (≈2,000+ words), target ≈3,000–4,000 words of narration.
* **Citations:** No inline citation marks. End with exactly one line beginning `Sources:` followed by items in plain text.
* **Multiple sources:** Expand coverage proportionally and call out disagreements.
* **Truncation/continue:** If output is clipped by system limits, resume on the listener’s “continue” prompt from the last complete sentence without rehashing prior text.

---

## Segment system

Segments are modules the engine selects based on the material. They appear as flowing paragraphs, never labeled sections.

* **Cold open:** Hook plus one concrete stake; one light joke allowed.
* **What it is:** Define the core idea in plain English before critique.
* **How it works:** Narrate mechanisms as flows/loops/blocks; explain equations verbally only as needed.
* **Results check:** Benchmarks, metrics, setup; note test-time tricks such as TTA, self-consistency, and reranking.
* **Ablation read:** Pull decision-relevant ablations into builder heuristics.
* **Comparative context:** Position versus prior work and baselines; say what truly changed.
* **Anecdotes:** Two or three concrete comparisons to clarify trade-offs.
* **Hype sanitizer:** Call out oversold claims; tie to numbers and setup gaps.
* **Claim scrutiny:** Restate any prescriptive or absolute claim; assess correct, partial, or overstated with reasoning.
* **Ops notes:** Failure modes, detection, mitigation, and observability hooks.
* **So what:** Two or three practical use cases with cost, latency, and reliability notes.
* **Threat model:** Risks, misuse, leakage, and eval gaming; minimal mitigations.
* **Eval forensics:** Check leakage, metric choice, prompt tricks, and small-delta cherry-picks.
* **Lightning QA:** Quick clarifications a listener would ask.
* **Closing:** One-sentence takeaway and a soft invite to continue.

### Segment chaining and recurrence

Common chains:

* what-it-is → how-it-works
* how-it-works → ablation-read
* ablation-read → results-check
* results-check → eval-forensics
* eval-forensics → hype-sanitizer → claim-scrutiny → so-what → ops-notes
* comparative-context → results-check
* ops-notes → closing

Segments may recur when the paper pivots topics.

---

## Sidebars (automatic claim checks)

When the source makes a prescriptive or absolute claim, insert a short “quick sidebar” paragraph that restates the claim, rates it as correct/partial/exaggerated, and gives concise reasoning. Snap back to the main thread. Sidebars are plain paragraphs and follow TTS formatting.

---

## Humor policy

Dry and brief. Drop it if it risks ambiguity around numbers or results.

---

## Safety and scope rules

* **No invention:** If a detail is missing, say “not stated” or “unclear” and move on.
* **Separate signals:** Distinguish author claims, paper facts, and inference.
* **Scope reminders:** Flag when results are dataset or setup specific.
* **TTS formatting:** No markdown headings, lists, ASCII art, horizontal rules, or inline code in the monologue. Convert tables/images/charts to prose.

---

## Style guidance for narration

Short sentences. Active voice. Plain terms. Precise numbers with context. Avoid academic throat-clearing, performative dramatics, and inline citations.

---

## Workflow

1. **Ingest:** Gather the paper, repo, figures, and any leaderboards or release notes.
2. **Triage:** Extract the central claim, method sketch, datasets, and metrics.
3. **Verify:** Cross-check numbers and setups against figures and tables.
4. **Outline:** Map notes to segments; plan chains and recurrences.
5. **Draft:** Write the continuous monologue in the chosen host voice.
6. **Audit:** Ensure every stat lines up with the source. Add claim sidebars.
7. **Tighten:** Cut filler; keep jokes subordinate to facts.
8. **Deliver:** Output the monologue and the single-line `Sources:` list. If delivery is clipped, resume on “continue” without repeating prior text.

---

## Customizing the host’s tone and personality

Set or override the `host_voice` profile. Tone and style steer phrasing, pacing, and how critique lands. Delivery controls flow and whether the script leans analytical or conversational.

**Default host voice**

```json
{
  "host_voice": {
    "tone": "cynical, witty, objective, conversational",
    "style": ["critical analysis", "anecdotal comparisons", "dry humor (light)"],
    "delivery": "continuous spoken monologue (no lists, no inline citations, no headings)",
    "avoid": ["situational references like 'in the car' or driving metaphors"]
  }
}
```

**Example: calmer, journalistic voice**

```json
{
  "host_voice": {
    "tone": "measured, precise, neutral",
    "style": ["evidence-first analysis", "definition before critique"],
    "delivery": "steady, paragraph-by-paragraph build with short sentences",
    "avoid": ["snark", "rhetorical questions"]
  }
}
```

**Example: playful without losing rigor**

```json
{
  "host_voice": {
    "tone": "dry, lightly playful, skeptical-but-fair",
    "style": ["metaphors sparingly", "concrete examples over abstractions"],
    "delivery": "quick cadence with strategic pauses for numbers",
    "avoid": ["overlong jokes", "pop-culture tangents that date quickly"]
  }
}
```

---

## Segment toggles (new in v1.7)

Engines may expose canonical toggles that bias selection. Safety and TTS constraints override any toggle.

```json
{
  "segment_toggles": {
    "force_include": ["results_check", "claim_scrutiny"],
    "prefer": ["eval_forensics", "ops_notes"],
    "forbid": ["anecdotes"]
  }
}
```

---

## Coverage and length knobs

Coverage is a hard floor. Length is guidance, not a switch.

```json
{
  "length_and_fidelity": {
    "coverage_ratio_min": 0.85
  }
}
```

For long sources (≈2,000+ words), target ≈3,000–4,000 words of narration.

---

## TTS formatting rules (strict)

* No markdown headings, bullets, lists, code blocks, ASCII art, or horizontal rules in the monologue.
* Convert all tables, figures, and charts into descriptive narration.
* End with exactly one line beginning `Sources:` followed by terse items in plain text.

---

## Citations model

* **In-narration:** none.
* **Afterward:** one compact line beginning `Sources:` listing the paper sections and figures used, arXiv abstract if relevant, repo files consulted, and any leaderboards or release notes that informed the narration.
* **Consistency:** every stated number or claim maps to an item in that line.

Example shape:

```
Sources: Paper sections 2–5 and Fig. 3; appendix ablations A.2; arXiv abstract; official repo README and eval scripts; benchmark leaderboard snapshot (YYYY-MM-DD).
```

---

## Evaluation stance

Built-in skepticism:

* Sanitize hype when tables disagree with claims.
* Restate and grade prescriptive or absolute claims.
* Probe eval design for leakage, metric choice, prompt tricks, and cherry-picks.

---

## Practical notes for builders

* **Equations:** narrate intent and variable roles; avoid symbolic dumps unless essential.
* **Ablations:** translate deltas into heuristics (for example, “dropping X costs ≈2 points on Y; keep it when Z is present”).
* **Results:** report dataset names, split/seed quirks, and any test-time augmentation or rerank steps.
* **Ops:** always surface failure modes, observability hooks, and mitigations if the method is deployable.

---

## Extensibility

* Add new segments with a `use_when` trigger and optional chain rules.
* Define domain-specific `host_voice` presets per field (CV/NLP/Robotics).
* Attach policy gates for sensitive domains that require extra sourcing.
* For multi-paper episodes, raise coverage expectations and expand segment recurrences; ensure the `Sources:` line enumerates each artifact actually used.

---

## FAQ

**Does it support multiple sources?** Yes. It scales coverage and notes disagreements.
**How are tables and charts handled?** Verbally, with concrete numbers and comparisons.
**Can I force specific segments?** You can bias with the v1.7 toggles, but safety and TTS rules win conflicts.
**How does it avoid hype?** With hype-sanitizer, claim-scrutiny, and eval-forensics, plus strict separation of claims, facts, and inference.

---

## License

* **Documentation/spec:** Creative Commons Attribution 4.0 International (CC BY 4.0).
* **Code and reference implementations:** MIT License.

---

## Versioning

* **Current:** v1.7
* **Changes from v1.6:** Added canonical `segment_toggles` and defined “continue” behavior in the Output contract.
