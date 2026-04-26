---
kind: source
title: How to Generate Tokens Faster: A vLLM Performance Model
slug: vllm-performance-model
source_ids:
  - raw-vllm-perf-model
status: active
raw_path: raw/vllm-perf-model.md
source_type: markdown
published: unknown
created: 2026-04-25
updated: 2026-04-25
---

# Summary

This article builds an engineering model for LLM inference performance using queueing language and then maps that model onto `vLLM` features. It distinguishes throughput from user-visible latency, adds TTFT and normalized latency to the metric set, and argues that service time, queueing delay, coherency, and service-channel count form a reusable systems framework for reasoning about serving.

# Key Claims

- Throughput and latency must be modeled together; one does not determine the other in parallel systems.
- LLM serving needs at least tokens-per-second, TTFT, and normalized latency to describe user-visible behavior.
- Queueing delay rises sharply after the system knee, so optimal operating points sit near but below saturation.
- `vLLM` improves performance mainly by increasing effective service channels and reducing interference through fine-grained scheduling and better KV memory use.
- Chunked prefill and continuous batching are useful because they reduce batch-induced coupling and improve scheduling granularity.

# Why It Matters

This source connects the papers to a more general systems vocabulary. It is useful because it turns serving discussions into transferable reasoning about workload, capacity, saturation, and interference rather than framework-specific folklore.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- Concept: [PagedAttention](../concepts/pagedattention.md)

# Open Questions

- The modeling language is strong at a systems level but does not produce a complete predictive formula for real mixed workloads.
- It treats `vLLM` as the anchor example, so some conclusions about scheduler knobs and saturation points remain engine-specific.
