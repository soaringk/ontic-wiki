---
kind: source
title: LLM Inference Performance Engineering Best Practices
slug: llm-inference-performance-engineering-best-practices
source_ids:
  - raw-llm-inference-performance-engineering-best-practices
status: active
raw_path: raw/LLM Inference Performance Engineering Best Practices.md
source_type: markdown
created: 2026-04-17
updated: 2026-04-17
---

# Summary

This source frames LLM inference as a systems trade-off problem rather than a single latency target. It separates prefill from decode, emphasizes time-to-first-token, time-per-output-token, and throughput as the core serving metrics, and argues that memory bandwidth, batching strategy, KV-cache management, and hardware topology dominate real deployment performance.

# Key Claims

- LLM generation splits into prompt prefill and autoregressive decode, and these phases stress hardware differently.
- Serving quality should be judged with TTFT, TPOT, total latency, and throughput rather than one aggregate speed number.
- Decode performance at small batch sizes is often memory-bandwidth-bound, so achieved memory bandwidth is a better predictor than peak FLOPs.
- Continuous batching is usually the best shared-service batching strategy, though static or dynamic batching can still fit offline or low-QPS workloads.
- Tensor parallelism, hardware bandwidth, interconnect quality, and quantization all trade off latency, throughput, memory fit, and model quality.

# Why It Matters

The source turns LLM serving into a measurable engineering discipline. It helps connect user-visible responsiveness, GPU cost efficiency, and hardware selection, while warning that naive scaling or quantization can hurt either efficiency or quality.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- Concept: [Model Bandwidth Utilization](../concepts/model-bandwidth-utilization.md)

# Open Questions

- The source is strong on performance heuristics but does not define concrete SLO targets, admission-control policy, or queueing models for mixed workloads.
- The quantization discussion is deliberately cautious and does not provide stable quality thresholds across model families.
