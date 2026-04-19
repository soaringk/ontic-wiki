---
kind: source
title: We're at AI's Halftime
slug: were-at-ais-halftime
source_ids:
  - raw-the-second-half
status: active
raw_path: raw/the-second-half.md
source_type: markdown
created: 2026-04-20
updated: 2026-04-20
---

# Summary

This essay argues that AI has entered a "second half" where the main bottleneck is no longer inventing new model families for narrow benchmarks, but designing evaluation setups that measure real-world utility. It claims that a working reinforcement-learning recipe now exists: large language priors, reasoning-as-action, and scalable fine-tuning can generalize across many tasks, so progress depends increasingly on asking the right questions and measuring the right outcomes.

# Key Claims

- Recent systems suggest that reinforcement learning now generalizes across a wider range of language-mediated tasks than many researchers expected.
- In practical RL systems, priors and environment design can matter more than algorithmic novelty; language pretraining supplies the transferable prior that earlier agents lacked.
- Reasoning can act as an internal action space that improves generalization and flexible test-time computation even when it does not immediately change the external environment.
- Classic benchmark hillclimbing is becoming less informative because a standardized recipe can saturate many existing evaluations faster than bespoke task-specific methods.
- The central unsolved problem is a utility gap: strong scores on exams, coding benchmarks, or games do not automatically translate into large real-world economic impact.
- Better evaluation should move away from purely autonomous, i.i.d. task scoring toward setups that include human interaction, sequential tasks, and accumulated familiarity with an environment.

# Why It Matters

The essay reframes current AI work from a contest over model architectures toward a contest over product-relevant evaluation and deployment environments. That matters for both research and operations: if benchmark design lags reality, teams may optimize for impressive scores while missing the harder problem of sustained usefulness in real workflows.

# Connections

- Topic: [Experiential AI](../topics/experiential-ai.md)
- Concept: [Streams of Experience](../concepts/streams-of-experience.md)
- Concept: [Utility Problem](../concepts/utility-problem.md)

# Open Questions

- Which evaluation designs best capture durable user value without becoming too expensive, noisy, or easy to game?
- If reasoning is treated as an internal action space, what are the right constraints and reward signals to keep it useful rather than bloated or misaligned?
- How should researchers compare progress across interactive, sequential, and environment-specific evaluations that do not reduce cleanly to a single benchmark number?
