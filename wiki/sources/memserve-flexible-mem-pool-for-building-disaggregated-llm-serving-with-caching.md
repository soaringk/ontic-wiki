---
kind: source
title: MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching
slug: memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching
source_ids:
  - raw-prefill-decode-separation-2406-17565v3
status: active
raw_path: raw/prefill-decode-separation/2406.17565v3.pdf
source_type: pdf
published: unknown
created: 2026-04-25
updated: 2026-04-27
---

# Summary

MemServe argues that once LLM serving becomes stateful, the real architectural problem is no longer only scheduling compute but managing KV cache as distributed data. It introduces `MemPool`, a shared memory substrate that lets context caching and prefill/decode disaggregation coexist inside one system.

# Key Claims

- Existing systems typically support either inter-request cache reuse or intra-request disaggregation well, but not both together.
- A distributed memory layer needs APIs for allocation, indexing, transfer, swap, and insert operations over KV cache.
- Prompt-token indexing is the most general way to support prefix reuse across sessions and instances.
- Disaggregated inference plus context caching requires decode-to-prefill cache return paths, not only prefill-to-decode transfer.
- Fine-grained paged layouts improve utilization but can create too many network calls unless memory and transport are co-optimized.

# Why It Matters

MemServe broadens the serving problem from per-request execution to long-lived state management. It is especially useful for understanding why prefix caching, swapping, and disaggregation are converging into one systems layer around KV cache.

# Connections

- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [PagedAttention](../concepts/pagedattention.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)

# Open Questions

- The paper makes KV management more general, but the resulting system complexity is materially higher than single-engine serving.
- It leaves open how broadly a generic memory substrate can remain efficient across different engines, block sizes, and network fabrics.
