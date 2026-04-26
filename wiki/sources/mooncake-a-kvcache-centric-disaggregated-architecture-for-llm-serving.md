---
kind: source
title: Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving
slug: mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving
source_ids:
  - raw-prefill-decode-separation-2407-00079v4
status: active
raw_path: raw/prefill-decode-separation/2407.00079v4.pdf
source_type: pdf
published: unknown
created: 2026-04-25
updated: 2026-04-25
---

# Summary

Mooncake treats KV cache as the central object of LLM serving rather than a side effect of model execution. It combines disaggregated prefill/decode pools with a distributed KV-cache layer over CPU DRAM and SSD, plus overload-aware scheduling, early rejection, and cache-block replication for a production MaaS workload.

# Key Claims

- Scheduling should optimize effective throughput under TTFT and TBT SLOs, not assume every request can or should be served.
- KV cache reuse, movement, replication, and eviction are central scheduling decisions, not mere implementation details.
- Long-context workloads justify a dedicated prefill pool with chunked or layer-wise transfer to reduce TTFT and VRAM pressure.
- Under heavy overload, early rejection can save wasted compute but needs prediction to avoid unstable oscillations.
- A lower-tier cache over CPU memory and SSD can expand usable context-cache capacity without more GPU memory.

# Why It Matters

Mooncake pushes the field toward production-style serving constraints: overload, admission control, and large reusable cache pools. It is valuable because it turns KV cache into the unit that ties together reuse, scheduling, and cost.

# Connections

- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- The architecture is compelling for long-context, cache-rich workloads, but its benefit depends heavily on cache-hit structure and available network bandwidth.
- The paper introduces strong heuristics for overload handling, yet the long-term stability and fairness of those policies remain partially empirical.
