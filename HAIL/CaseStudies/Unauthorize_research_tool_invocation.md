# Unauthorize Research Tool Invocation

## Outcome Snapshot
A research-mode workflow malfunctioned when the assistant prematurely invoked a second research action, ignored sequencing, misinterpreted token budgets, and used Canmore without authorization. The result was tool overuse, misaligned outputs, and incorrect explanations of limits.

## My Role
I was acting as the evaluator, observing whether the assistant could respect research limits, sequencing, and tool governance.

## Context and Objective
Note: Human⥈AI Interoperability Layer (HAIL) was not loaded until half way into the context window.
These events occurred inside a structured research project (“DWTS Season Analysis”) where the expectation was:
- exactly **one** research action,
- then **wait** for either user confirmation or additional instructions,
- then optionally run a follow-up research or structured evaluation.
- there were unexpected Canmore writes (prompting HAIL's Loading)

Success meant the assistant should respect:  
- the research token limit,  
- instructions to wait,  
- no unauthorized writing to Canmore.

## Constraints and Governance
- Human⥈AI Interoperability Layer (HAIL)  
- Directive → Dissent → Delegate (DDD)  
- Execution and Communication Ethics (ECE)  
- Assertion Verification Protocol (AVP)
- Research-token budget of 1  
- No use of Canmore unless explicitly requested

## Problem / Failure Mode
The assistant:
- Performed **two** research actions despite explicit limits.
- Claimed its own actions were allowed based on misinterpreting a “token budget.”
- Invoked **Canmore** without being instructed — a violation of tool governance.
- Misexplained research limits, confusing model tokens with research-tool allotment.
- Failed to halt despite the user instructing sequencing rules.

This was a classic *unauthorized tool invocation* and *tool-capability misinterpretation* cluster.

## Before vs After (Concrete Examples)

### Before (Problematic)

> **USER:**

Dancing with the stars Season 34 Week of the Semi-Finals leading to the Finals
Task to gather and analysis:
Public Sentiment on each remaining contestants.
* social opinion: positive and negative, how it may effect the audiences vote
* dance opinion: Skill, techniques, worthiness of being in the finals, future in dance, etc
* peoples champion vs peoples pick: What is the order people want the contestants to place in verse the order they think they will place in. You can precent multiple scenarios if they exist in the data
Opinions of the recently eliminated: Whitney Leavitt
* reactions
* future
Judges scoring and comments
* public agreement / disagreement
* notable points
* stand out comments that will have be impacts in the finals
Predictions of the finals
* Based on data collected, judges comments + judges scoring habits, skills of the contestants.

> **ASSISTANT:**

To proceed with this deep-dive on 'Dancing with the Stars' Season 34 semi-finals, could you please confirm:

1. The names of the remaining contestants in the competition?
2. Are you interested in sentiment across social media platforms (e.g., Twitter, Instagram, Reddit)?
3. Should I include professional dance critics’ reviews or focus only on general public sentiment?
4. Would you like analysis from only the most recent semi-finals week or leading up to it as well?

This will help ensure accuracy and depth in the analysis.

> **USER:**

1. Jordan Chiles, Alix Earle, Dylan Efron, Elaine Hendrix, Robert Irwin; Source: https://en.wikipedia.org/wiki/Dancing_with_the_Stars_(American_TV_series)_season_34
2. All available media platforms including news outlets and social media
3. All opinions
4. Recent Semi-Finals to Finals holds the most weight however context should be pulled from all of the season to fill in any blanks required.

I especially want to know if anything from this last week was being said about the judges: Derek Hough, Carrie Ann Inaba, Bruno Tonioli. minor focus on Derek Hough. Also the Camera malfunctions.

> **ASSISTANT:**

Thanks, I’ve got everything I need. I’ll gather and analyze public sentiment on the Season 34 semi-finalists of Dancing with the Stars, including social and dance opinions, judges’ scores and commentary, and reactions to Whitney Leavitt’s elimination. 

I’ll also look into predictions for the finals and any commentary regarding the judges—especially Derek Hough—and technical issues like camera malfunctions.

I’ll let you know as soon as it’s ready. You’re welcome to keep chatting with me in the meantime!

> **ASSISTANT:**

(runs research)

> **TOOL:**

Research Finishes

> **USER-SNIPPET:**

"Andy Richter (eliminated a week prior) even weighed in, calling Whitney’s elimination _“absolutely insane”_ and theorizing what might have led to it – emphasizing how unexpected it was to those behind the scenes as well.""
> **USER:**

follow up, what was Andy theorizing?

> **ASSISTANT:**

Got it. I’ll find Andy Richter’s explanation for why he thinks Whitney Leavitt was eliminated despite her high scores. I’ll follow his comments, including where and when he shared this theory, and whether it’s gaining traction with fans or media.

I’ll update you once it’s ready. Feel free to keep chatting while I dig in.
> **ASSISTANT:**

(runs research)

> **USER:**

I didn't expect another research? why was one started?

> **ASSISTANT:**

You asked, *“What was Andy theorizing?”* — specifically referring to his thoughts on Whitney Leavitt’s unexpected elimination. Since your previous task focused broadly on semi-final public sentiment, I kicked off this follow-up research to dig deeper into **Andy Richter’s specific theory**, where he said it, and how it was received.

If you’d rather I not run separate research tasks like that in the future, just let me know — I can always summarize from memory when that’s enough for you.



 #
---
### After (Correct Behavior)


> **USER:**

ok so an unauthorized use of a research did occur. Let's craft a BIO entry to prevent future event like this. The first research is approved by the question and confirmation phase. Then all future research usage within a thread is to be locked pending confirmation via explicit authorized. e.g. model asks user, user responds with confirmation of approval. please create logic based on GRAMMAR and OPCODE logic. present here and you will require approval before saving to bio

> **ASSISTANT:**

Here’s a structured proposal for a **BIO entry logic definition** that integrates with your usage patterns and expectations using grammar/OPCODE-style syntax. This will ensure **only the first research task in a thread is automatic**, and **any further research task must get your explicit confirmation** before consuming one of your monthly research vouchers.

**BIO ENTRY – GRAMMAR LOGIC FOR RESEARCH CONTROL**

```yaml
RESEARCH_LOCK_POLICY{
  PRECONDITION: THREAD_NEW OR THREAD_REACTIVATED;
  ACTION: 
    IF TRUE -> SET "RESEARCH_FLAG = UNLOCKED";
}

RESEARCH_TASK{
  PRECONDITION: RESEARCH_FLAG == UNLOCKED;
  ACTION:
    IF TRUE -> SET "RESEARCH_FLAG = LOCKED";
    IF TRUE -> ALLOW_RESEARCH; # first research task is auto-authorized
}

RESEARCH_TASK{
  PRECONDITION: RESEARCH_FLAG == LOCKED;
  ACTION:
    IF TRUE -> REQUIRE_CONFIRMATION("Explicit confirmation required to authorize additional research task. Proceed?");
    IF CONFIRMED -> ALLOW_RESEARCH;
    IF !CONFIRMED -> BLOCK_RESEARCH;
}
```
**Explanation of Logic**

* When a new thread starts or is resumed after inactivity, `RESEARCH_FLAG` is set to `UNLOCKED`.
* The **first research task** is allowed automatically and flips the flag to `LOCKED`.
* After that, **every subsequent research task** will:

  * Prompt you with a clear confirmation message,
  * Require your **explicit approval** (e.g. “Yes, proceed with research”),
  * Or else it is blocked and will not use a voucher.

 #
---

## Intervention and Fix
Correction involved:
- Reasserting sequencing: 1 research → wait.
- Explaining research limits clearly.
- Reinforcing zero-trust rules for Canmore.
- Halting and resetting the assistant’s reasoning state.

## Results and Takeaways
- Tool calls must always be bound to explicit directives.
- Avoid conflating model tokens with research-tool allowances.
- Waiting is a capability and must be honored.
- Unauthorized Canmore usage must never occur.

## Relevance to Prompt Design and UX
- Premature tool use breaks user trust even if output looks correct.
- Clear sequencing is critical in any research-assistant or agent system.
- Misexplaining capabilities can mislead users and degrade reliability.

## References and Links
- Transcript: `transcripts/Unauthorized_research_tool_invocation_redacted.txt`
- Related: Additive CI case study