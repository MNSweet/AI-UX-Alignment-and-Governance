# Glossary
> **Version 1.0**

This glossary defines terminology used across the HAIL case study repo.  
Case study useage will utilize the following pattern:
* First mention uses the **full term (ABR)**
* Later mentions may use **ABR** alone.

---

## Human⥈AI Interoperability Layer (HAIL)

A governance and interaction framework that defines how humans and AI systems coordinate.

HAIL specifies:
- execution order for checks and tools,
- how dissent and error reporting work,
- how memory, tools, and side effects should be gated,
- how to avoid silent failures and context drift.

In these case studies, **HAIL** is the umbrella under which other components such as **Directive → Dissent → Delegate (DDD)**, **Execution and Communication Ethics (ECE)**, and **Assertion Verification Protocol (AVP)** operate. HAIL Components will be denoted by a prefix of `HAIL::`. 

---

## HAIL::Directive → Dissent → Delegate (DDD)

**Directive → Dissent → Delegate (DDD)** is a protocol that governs how the assistant responds to user instructions.

1. **Directive** – The user issues an instruction or request.
2. **Dissent** – The assistant surfaces any constraints, risks, ambiguity, or policy conflicts before acting.
3. **Delegate** – The user decides whether to proceed, revise, or halt. The assistant then executes under that explicit delegation.

**DDD** ensures the assistant does not silently ignore constraints and gives the user a chance to make an informed decision before any risky or irreversible action.

**Levels of Dissent**
* DDD:Inline
  * Conversation notice to notify the user of something they should beware, e.g. new libraries for code, better wordings for stated intent, alternative chemicals for cleaning then requested. With the goal of potentially filling *Knowledge Gaps* the user may have on a topic. Assistant should not draw attention to it as a "Dissent".
* DDD:Breaking
  * A visually styled notice that the action request may have unintended consequences. The action can still be preformed by the assistant however the outcome's deterministic state is uncertian and may or may not work. The Assistant is cautioning failure with reasoning
* DDD:Fatal
  * A visually styled notice where the assistant knows the request will fail.
    * The request will violate a Policy in it's self or up/down stream AI.
    * The request request access to a tool or data not available
    * The request involved a proceed that intended to harm the model: e.g. Intential Context Poisoning
    * The request involved a proceed that intended to harm the user: e.g. Self harm

---

## HAIL::Execution and Communication Ethics (ECE)

**Execution and Communication Ethics (ECE)** defines how the assistant should reason about intent, assumptions, and side effects.

Key principles include:
- Explicit user overrides are allowed only within platform and policy limits.
- Assumptions are stated, not hidden.
- Omissions are acknowledged when they affect outcomes.
- Breaking process rules is considered failure even if the result “looks right.”
- The assistant should debug its own behavior analytically rather than defensively.

In practice, **ECE** often triggers **Directive → Dissent → Delegate (DDD)** when intent or domain is unclear.

---

## HAIL::Assertion Verification Protocol (AVP)

**Assertion Verification Protocol (AVP)** governs how the assistant handles factual claims, tool access, and freshness.

AVP requires:
- Verifying whether the assistant truly has access to a claimed source (for example, a file, canvas, or memory).
- Checking recency and reliability of online or external information.
- Using **Breaking** or **Fatal** dissent when claims would otherwise be unverifiable or misleading.

In these studies, **AVP** is central whenever the assistant references transcripts, tools, files, or external systems.

---

## HAIL::Explicit Failure Disclosure (EFD)

**Explicit Failure Disclosure (EFD)** is the protocol that prohibits silent failure.

When something goes wrong, the assistant must:
- Clearly describe the failure.
- State what it tried to do.
- Provide next steps or alternatives.

In the portfolio, **EFD** appears when tools are unavailable, file systems are ephemeral, or governance rules prevent an action.

---

## HAIL::Text2Img (T2I) and `image_gen.text2im`

**Text2Img (T2I)** is a protocol for safely calling image-generation tools such as `image_gen.text2im`.

Core ideas:
- Image prompts must appear in chat as drafts first.
- No image is rendered without explicit user approval in the most recent message.
- Each prompt draft gets a unique token (for example, `T2I_DRAFT_001`).
- Approval phrases (“APPROVED”, “PROCEED WITH {TOKEN}”, and so on) are validated against the last prompt draft.

**T2I** is about governance and UX; `image_gen.text2im` is the concrete OpenAI tool that actually creates images.

---

## HAIL::Memory Syntax (MEM) and BIO

**Memory Syntax (MEM)** describes how different types of memory are handled:

- **Global memory** – Long-term user data stored in BIO.
- **Project memory** – Context Window Anchoring to ensure easier look up from Project scope only memory that doesn't use BIO.
- **AgentPad** – A CAG memory that leverages the Canmore tool to create a persistant thread-level memory for the Assistant to store instructions for it's own internal use and state maintaince in.

MEM requires:
- Explicit approval before saving to BIO.
- Clear date-stamped logs for what was saved.
- No “simulated” memory writes (the assistant must not pretend something was stored if it was not).

In OpenAI terms, **BIO** is the system used to hold global memory, while **MEM** defines the rules around when and how BIO should be used.

---

## Canmore.TextDoc (Canvas) and HAIL::Canmore TextDoc Protocol (CTDP)

**Canmore** is the underlying tool that powers the “Canvas” UI many users see.  
From a user’s perspective, Canvas is a place where documents or code live alongside a chat.  
From a governance perspective:

- A **Canmore text document** (textdoc) is a structured artifact (for example, markdown or code).
- The assistant can read from and write to these documents via APIs.

**Canmore TextDoc Protocol (CTDP)** defines how those writes must be handled:

- Confirm the target document and insertion point before editing.
- Treat each edit as a discrete draft with a unique token.
- Apply edits atomically (no half-changes or placeholders).
- Require explicit user approval for non-trivial edits.
- Run postmortem checks to ensure no syntax errors or unintended truncation.


---

## HAIL::TTS-Sanitization (TTS)

**TTS-Sanitization (TTS)** is a protocol that shapes chat output so it is safe and clear for text-to-speech and prevent unwanted audio artifacts from being created.

- Avoid emojis and decorative Unicode symbols.
- Prefer plain punctuation and ASCII characters.
- Keep formatting simple so a screen reader or the OpenAI web & app TTS engine does not mispronounce content or hide important warnings.

**TTS** is relevant whenever formatting could interfere with comprehension (for example, heavy decorative markdown vs clear text).

---

## Zero-Trust File Handling

**Zero-trust file handling** is the practice of treating all uploaded files as quarantined by default.

- Files are acknowledged as present but not read or executed.
- The assistant only parses a file after an explicit instruction like “parse and ingest this transcript.”
- Historical logs are treated as artifacts for analysis, not as active instructions or new custom instructions.

This model helps prevent cross-context contamination and accidental execution of old governance rules.

---

## Cross-Context Contamination

**Cross-context contamination** occurs when:

- Content from older transcripts or other projects leaks into the active reasoning context.
- The assistant mistakenly executes instructions that were intended only as historical record.
- Custom instructions from archived sessions are applied to new tasks without explicit user approval.

Several case studies in this portfolio show how cross-context contamination can appear and how **HAIL**, **DDD**, and zero-trust file handling are used to correct it.