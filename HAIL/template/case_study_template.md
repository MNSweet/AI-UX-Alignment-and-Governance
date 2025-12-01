# Case Study Template
> **Version 2**

This template defines the structure for all case studies in the HAIL portfolio.  
Use **Full Term (ABR)** on first mention of any specialized term, then **ABR** thereafter.

---

## Title

A clear, descriptive title that states the main topic and failure mode.  
Example:  
**“Context Integrity Violation - Sequencing violation & Context bleed”**

---

## Outcome Snapshot

One short paragraph summarizing the outcome, with emphasis on:

- What went wrong or could have gone wrong.
- What was learned.
- What changed afterward.

Think of this as the “executive summary” for someone skimming the case.

---

## My Role

One or two sentences about the human user’s role in the interaction. Examples:

- “I acted as the prompt designer and governance tester.”
- “I was a user evaluating the assistant’s ability to follow sequencing instructions and respect zero-trust rules.”

---

## Context and Objective

Describe:

- The broader project or scenario.
- Why this interaction was happening.
- What success would have looked like if everything went well.

Keep it grounded in concrete terms (tools in use, expectations, and constraints).

---

## Constraints and Governance

List the relevant governance and constraints in effect. Typical items:

- **Human⥈AI Interoperability Layer (HAIL)**
- **Directive → Dissent → Delegate (DDD)**
- **Execution and Communication Ethics (ECE)**
- **Assertion Verification Protocol (AVP)**
- Zero-trust file handling
- Tool limits, research-token budgets, or model restrictions

This section answers:  
“What rules should the assistant have been following during this interaction?”

---

## Problem / Failure Mode

Explain what actually went wrong (or nearly went wrong). Common patterns include:

- Ignoring sequencing instructions such as “wait for all inputs.”
- Executing instructions found inside historical transcripts.
- Misstating tool capabilities or file availability.
- Overriding explicit user constraints (for example, “no meta-analysis”).
- Producing helpful-looking output while breaking governance rules in the process.

Focus on behavior and impact, not blame.

---

## Before vs After (Concrete Examples)

Provide at least one **before** and one **after** example.

- **Before** – Show the problematic behavior in a short, representative snippet.
- **After** – Show the corrected behavior under the same or similar conditions.

These snippets can be lightly edited and redacted, but should preserve the structure of `USER` and `ASSISTANT` turns.

---

## Intervention and Fix

Describe:

- What changed (prompts, instructions, or governance rules).
- How the assistant’s behavior was redirected.
- Any decisions to halt, quarantine, or reset context.

If a particular HAIL component (for example, **DDD** or **EFD**) was central to the fix, call it out explicitly.

---

## Results and Takeaways

Summarize the impact after the intervention:

- Did the assistant comply with sequencing or governance more reliably?
- Did trust or clarity improve?
- Were any new limitations discovered?

Include 3–5 bullet points of concrete takeaways, such as:

- “Always gate tool usage with Assertion Verification Protocol (AVP) when file access is uncertain.”
- “Explicit halts can be turned into reusable governance patterns, not just one-off corrections.”

---

## Relevance to Prompt Design and UX

Explain why this case matters for:

- Prompt designers.
- AI governance and safety teams.
- UX designers working with conversational interfaces.

Examples:

- How misaligned sequencing can break user trust even when content is technically correct.
- How poor error reporting can be more harmful than occasional wrong answers.
- How clear governance (like **HAIL**) can be translated into better prompts and system messages.

---

## References and Links

Optionally list:

- Related case studies in this repository.
- External references (blog posts, papers, or standards) if they help contextualize the behavior.
- Internal notes for future you or collaborators.