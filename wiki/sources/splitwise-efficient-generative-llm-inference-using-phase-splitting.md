---
kind: source
title: Splitwise: Efficient Generative LLM Inference Using Phase Splitting
slug: splitwise-efficient-generative-llm-inference-using-phase-splitting
source_ids:
  - raw-prefill-decode-separation-2311-18677v2
status: active
raw_path: raw/prefill-decode-separation/2311.18677v2.pdf
source_type: pdf
published: unknown
created: 2026-04-25
updated: 2026-04-25
---

# Summary

Splitwise argues that prefill and token generation should not merely be scheduled differently but can run on different machines altogether. It frames phase splitting as a way to match compute-heavy prefill with newer GPUs and memory-bound decode with cheaper or lower-power hardware, provided KV-cache transfer is fast enough.

# Key Claims

- Prompt processing and token generation have materially different compute, memory, latency, and power profiles.
- Decode often underuses the newest GPUs' compute capability while still consuming cost and power.
- Separating phases enables heterogeneous clusters tuned for throughput per dollar or throughput per watt.
- Batch behavior differs by phase: prompt batching hits compute limits quickly, while decode keeps benefiting from larger batches until memory limits dominate.
- Fast interconnects can make cross-machine KV transfer cheap enough to justify disaggregation.

# Why It Matters

This source pushes disaggregation from a scheduler detail into a datacenter-level resource-allocation decision. It is especially important for understanding why prefill/decode separation is not only about latency, but also about hardware economics.

# Connections

- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- The gains depend heavily on cluster interconnect quality and workload mix, so the design is not obviously superior on weaker networks or short-output workloads.
- The paper does not deeply address prefix caching or how shared historical KV state changes disaggregation decisions.
