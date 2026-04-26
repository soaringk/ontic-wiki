---
kind: source
title: DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving
slug: distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving
source_ids:
  - raw-prefill-decode-separation-2401-09670v3
status: active
raw_path: raw/prefill-decode-separation/2401.09670v3.pdf
source_type: pdf
published: unknown
created: 2026-04-25
updated: 2026-04-25
---

# Summary

DistServe treats LLM serving as a goodput optimization problem under both TTFT and TPOT constraints. Its thesis is that colocated prefill and decode create both interference and resource-coupling, so the system should disaggregate them and optimize GPU allocation plus parallelism separately for each phase.

# Key Claims

- Continuous batching across prefill and decode creates unavoidable TTFT-versus-TPOT trade-offs.
- Colocation couples resource allocation and parallelism settings for phases that want different execution strategies.
- Prefill behaves more like a compute-bound queueing problem, while decode wants larger memory-backed batches.
- Goodput should be defined as the maximum request rate that still satisfies latency SLO attainment.
- Placement and bandwidth still matter, but modern GPU clusters often make transfer overhead manageable.

# Why It Matters

DistServe supplies a stronger optimization vocabulary than pure throughput. It links disaggregation to queueing theory, SLO attainment, and per-GPU efficiency, which makes it useful for capacity planning rather than only kernel-level reasoning.

# Connections

- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

# Open Questions

- The framework assumes explicit TTFT and TPOT targets, but real products often need richer objectives such as queue fairness, admission control, and streaming quality.
- It analyzes disaggregation mainly without persistent cross-request cache reuse, leaving open how strong prefix caching changes the optimum.
