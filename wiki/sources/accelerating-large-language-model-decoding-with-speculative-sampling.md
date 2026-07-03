---
kind: source
title: Accelerating Large Language Model Decoding with Speculative Sampling
slug: accelerating-large-language-model-decoding-with-speculative-sampling
source_ids:
  - raw-2302-01318v1
status: active
raw_path: raw/2302.01318v1.pdf
source_type: pdf
parser: mineru
published: 2023-02-02
created: 2026-06-30
updated: 2026-06-30
---

# Summary

This DeepMind paper presents speculative sampling for reducing large-language-model decode latency. A faster draft model proposes several tokens, the larger target model scores the short continuation in parallel, and a modified rejection-sampling rule accepts or repairs tokens so the final samples preserve the target model distribution within numerical limits.

# Key Claims

- Transformer decoding is often memory-bandwidth-bound and serial, especially for small-batch latency-critical serving of very large models.
- Scoring a short draft continuation with the target model can cost about the same latency as scoring one next token because parameters, KV cache reads, and model-parallel all-reduces dominate.
- Modified rejection sampling accepts draft tokens with probability based on the target/draft probability ratio and samples from the positive residual distribution after a rejection.
- Correct speculative sampling can preserve the target model's sampling distribution rather than merely approximate or distill it.
- Draft model design is a systems problem: the best draft is not necessarily a conventionally optimal smaller model, because device topology, layer count, communication, and latency dominate.
- On Chinchilla 70B with a 4B draft model, the paper reports roughly 2x to 2.5x decode speedups on XSum and HumanEval without benchmark-quality degradation.

# Why It Matters

Speculative sampling is a core decode-side acceleration technique because it attacks the sequential one-token-per-target-call bottleneck without requiring target-model retraining or a changed output distribution. It also makes acceptance rate and draft-model serving topology first-class capacity-planning variables.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Concept: [Speculative Decoding](../concepts/speculative-decoding.md)
- Concept: [Token Sampling Strategies](../concepts/token-sampling-strategies.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- Acceptance rate and latency gains vary by domain, decoding method, and lookahead length; larger drafts can increase mean speed while worsening tail latency variance.
- The paper focuses on batch-size-one latency; production gains under continuous batching and mixed workloads require separate validation.
