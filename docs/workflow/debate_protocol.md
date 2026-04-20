# Debate Protocol

## Purpose

Use the debate area to validate curated sources, stress-test interpretations, and polish arguments before promoting them into durable wiki pages. The goal is epistemic quality control, not performative disagreement.

The protocol exists because a single agent can be both persuasive and wrong. When a conclusion conflicts with the user's judgment, the debate workflow should make disagreement explicit, collect competing readings, and preserve enough evidence for the user to decide.

The protocol should reduce three common failures:

- overstating what a source claims
- mixing facts, axioms, hypotheses, interpretations, and recommendations
- promoting interesting but weak arguments into durable wiki pages too early

## Placement

- `wiki/debates/` contains curated debate briefs and argument maps.
- `wiki/synthesis/` contains durable resolved conclusions.
- Raw multi-agent transcripts should not be stored in `wiki/debates/` by default. If full traces are ever needed, store them separately under machine state, not as polished wiki knowledge.

Debate pages are interpretive workbench pages. They are not source pages, and they should not become parallel topic or synthesis pages.

## Adjudication Boundary

For now, the user is the adjudicator for debates.

Agents may:

- open or update a debate page
- extract claims from sources
- argue for and against candidate interpretations
- classify claims as facts, axioms, hypotheses, interpretations, or recommendations
- identify what each side would need to concede
- propose promotion targets and candidate wording

Agents must not:

- mark a contested debate as decided without explicit user instruction
- present their own reconciliation as the final decision when they also participated in the debate
- promote debate conclusions into source/topic/concept/synthesis pages unless the user has accepted the conclusion or asked for the promotion
- collapse minority or skeptical views merely because one agent produced a cleaner narrative

The Reconciler role maps agreements, disagreements, and possible staged resolutions; it is not the judge. The Editor role drafts candidate wiki wording; it is not the judge. The user's decision, not an agent's confidence, closes the debate.

## When To Use

Use the protocol when:

- multiple sources appear to conflict
- a synthesis page makes a durable comparative argument
- a topic or concept page depends on contested interpretation
- a source page contains strong claims that need careful wording
- chronology, publication timing, or source provenance matters

Do not require the full protocol for routine source summaries, mechanical link repairs, or narrow factual updates.

## Debate Page Shape

Recommended frontmatter:

```yaml
kind: debate
title: ...
slug: ...
status: active|awaiting_user|decided|archived
adjudicator: user
decision: undecided|accepted|rejected|promoted|archived
created: ...
updated: ...
sources:
  - sources/...
related_topics:
  - topics/...
related_synthesis:
  - synthesis/...
promoted_to:
  - synthesis/...
```

Recommended sections:

1. Debate Question
2. Source Set
3. Candidate Claim
4. Extracted Claims
5. Advocate Case
6. Skeptical Case
7. Reconciliation Map
8. Claim Classification
9. Agent Recommendations
10. User Decision

## Agent Roles

- **Curator:** selects the source set, identifies the claim being tested, checks source metadata, and produces the initial argument map.
- **Advocate:** builds the strongest source-backed version of the candidate argument, while distinguishing direct source claims from interpretation.
- **Skeptic:** looks for overreach, missing counterevidence, chronology errors, weak causal claims, and category mistakes.
- **Reconciler:** separates real contradiction from compatible framing differences, staged reconciliation, scope limits, and false binaries.
- **Editor:** converts the surviving argument into compact wiki prose appropriate for the target page type.
- **Archivist, optional:** verifies local links, raw paths, source metadata, and whether disputed claims are traceable to source pages or raw material.

For multi-agent work, run at least an Advocate and Skeptic independently before reconciliation. For high-value arguments, give later agents the prior rounds so they can respond to each other rather than merely produce isolated summaries.

No role is allowed to close the debate. If the main agent has argued for one side, it should explicitly separate its own view from the debate record and present the user with the decision points.

## Round Structure

### Round 0: Setup

Inputs:

- source pages involved
- raw files only when needed to verify disputed claims
- candidate claim or debate question
- target output page type: source, topic, concept, synthesis, or debate

Output:

- one-sentence debate question
- source list
- initial classification of the claim as fact, axiom, hypothesis, interpretation, or recommendation

### Round 1: Claim Extraction

Extract the strongest relevant claims from each source.

Record each claim as:

```text
Claim:
Source:
Evidence type: direct statement | paraphrase | inferred implication
Published date: known | unknown | ambiguous
Confidence: high | medium | low
Notes:
```

Use each source's actual `published` metadata when chronology matters. Do not substitute local `created`, `updated`, ingest, or report dates.

### Round 2: Advocate Case

Build the strongest concise argument using only admissible evidence.

Requirements:

- cite local source pages where possible
- mark interpretation explicitly
- avoid importing external context unless the task asks for it
- state what would weaken the argument

### Round 3: Skeptical Case

Challenge the argument.

Required checks:

- Does the source actually say this?
- Is the wording stronger than the evidence?
- Are two concepts being conflated?
- Is correlation being treated as causation?
- Is a chronology-sensitive claim using actual publication dates?
- Are missing sources or counterexamples material?
- Is the disagreement about substance, wording, emphasis, scope, or assumptions?

### Round 4: Classification

Classify each contested claim:

- **Fact:** directly supported by a source or stable local wiki content.
- **Axiom:** a governing assumption or value judgment; attribute it or frame it as a premise.
- **Hypothesis:** plausible but unsettled; phrase conditionally.
- **Interpretation:** the wiki's grounded reading of how sources relate; do not present it as a source's own claim.
- **Recommendation:** an action for study, research direction, or page maintenance; separate it from descriptive claims.

The classification round should also identify the disagreement type:

- **Source disagreement:** sources directly make incompatible claims.
- **Assumption disagreement:** sources rely on different starting premises.
- **Scope disagreement:** claims apply to different domains, timelines, or levels of abstraction.
- **Evidentiary disagreement:** sources use different standards of proof or reliability.
- **Terminology disagreement:** apparent conflict depends mainly on word choice.
- **Open hypothesis:** evidence is insufficient to decide.

### Round 5: Revision

Rewrite the argument using the classifications:

- facts get direct attribution
- axioms are named as assumptions
- hypotheses are hedged
- interpretations are framed as synthesis
- recommendations are placed in action-oriented sections
- unresolved disagreements remain visible

### Round 6: Agent Recommendations

Agents propose one outcome, but do not execute it unless the user explicitly approves:

- **Reject:** insufficient support or too speculative
- **Hold:** useful but unresolved; keep as debate note
- **Promote to source page:** improves one source's summary, key claims, connections, or open questions
- **Promote to concept page:** names a reusable idea across sources
- **Promote to topic page:** updates a broader study area
- **Promote to synthesis page:** preserves a durable comparative argument

The debate should then move to `status: awaiting_user` unless the user has already provided an explicit decision.

### Round 7: User Decision

Only the user may close the debate in the current workflow.

The user can decide:

- **Accepted:** the debate conclusion is accepted and may be promoted.
- **Rejected:** the proposed conclusion is not accepted; preserve only useful objections or discard the debate.
- **Hold:** the debate remains open because the evidence is insufficient.
- **Promote with edits:** the user accepts a direction but requires wording or scope changes.
- **Archive:** the debate is no longer useful as a workbench artifact.

After a user decision:

- update frontmatter `status` and `decision`
- promote accepted conclusions into the appropriate durable pages
- keep debate pages concise and link them to the promoted page when retained
- remove or archive obsolete debate pages when the user says they are no longer useful

## Evidence Rules

Admissible evidence:

- local source pages under `wiki/sources/`
- raw source material under `raw/`, read-only
- existing topic, concept, debate, or synthesis pages as secondary wiki context
- source `published` metadata when chronology matters

Evidence discipline:

- Prefer local wiki citations first.
- Verify disputed claims against raw material when summaries are ambiguous.
- Separate quotation, paraphrase, and inference.
- Do not cite a source for a claim it merely resembles.
- Do not promote a claim that depends on unavailable evidence unless uncertainty is explicit.

## Promotion Criteria

A claim or argument may enter durable wiki pages only if the user has accepted promotion and the material is:

- **Traceable:** important claims link back to source pages or raw material.
- **Typed:** facts, axioms, hypotheses, and interpretations are distinguishable in wording.
- **Scoped:** the claim says where it applies and avoids unjustified universal language.
- **Non-duplicative:** it updates an existing page when possible.
- **Chronology-safe:** time-sensitive claims use actual source publication metadata where available.
- **Stable enough:** it is likely to remain useful beyond the immediate conversation.
- **Compact:** durable pages get the conclusion and reasoning, not the full debate transcript.
- **Connected:** promoted material links to relevant source, topic, concept, debate, or synthesis pages.

## Page-Type Boundaries

- Source pages stay descriptive and source-local.
- Topic pages mention live tensions briefly and link to debate or synthesis pages.
- Concept pages hold reusable ideas, not one-off source comparisons.
- Debate pages preserve competing positions, evidence, objections, and promotion decisions.
- Synthesis pages hold the durable answer once a debate has a stable conclusion.

If a debate and synthesis contain the same bottom line after user acceptance, the synthesis is canonical and the debate should point to it as the promoted conclusion.

## Lint Treatment

For now, lint jobs may inspect debate pages but must not close them.

Lint may:

- report debate pages in inventory
- flag broken links, missing source citations, missing frontmatter, stale status, or debate/synthesis duplication
- suggest that a debate is ready for user decision

Lint must not:

- mark `status: decided`
- promote conclusions into synthesis/topic/concept/source pages
- delete or archive a debate page
- treat an agent recommendation as a user decision

If future automation should close debates, that must be a deliberate workflow change. Until then, debate closure is user-owned.
