---
kind: source
title: Orca: A Distributed Serving System for Transformer-Based Generative Models
slug: orca-a-distributed-serving-system-for-transformer-based-generative-models
source_ids:
  - raw-orca-a-distributed-serving-system-for-transformer-based-generative-models
status: active
raw_path: raw/Orca A Distributed Serving System for Transformer-Based Generative Models.pdf
source_type: pdf
published: 2022-07
created: 2026-04-25
updated: 2026-04-25
---

# Summary

ORCA reframes generative-model serving as an iteration-scheduled workload rather than a request-scheduled one. Its central idea is that the scheduler should regain control after every token-generation step so finished requests can leave early, new ones can join quickly, and batching can be selective instead of all-or-nothing.

# Key Claims

- Request-level scheduling is a bad fit for autoregressive generation because different requests finish at different iterations.
- Iteration-level scheduling reduces queueing delay for late arrivals and unnecessary waiting for early finishers.
- Transformer serving can still batch efficiently if only the operations that benefit from batching are batched.
- Selective batching works because attention has shape irregularities that other per-token operations do not.
- Large distributed models need explicit scheduling awareness of KV-state memory, not just raw compute placement.

# Why It Matters

ORCA provides a durable systems lens for LLM serving: token streaming changes the right scheduling granularity. Later systems differ on memory layout and phase placement, but many still inherit this basic shift from request-level to iteration-level control.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- ORCA predates paged KV-cache management, so its reservation-heavy memory model leaves open how much more throughput later memory systems can unlock.
- Selective batching clarifies execution structure, but the paper does not fully resolve when mixed prefill/decode batching should be abandoned for disaggregated deployment.
