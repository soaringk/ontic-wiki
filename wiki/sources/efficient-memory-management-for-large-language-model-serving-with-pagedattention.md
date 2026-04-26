---
kind: source
title: Efficient Memory Management for Large Language Model Serving with PagedAttention
slug: efficient-memory-management-for-large-language-model-serving-with-pagedattention
source_ids:
  - raw-efficient-memory-management-for-large-language-model-serving-with-pagedattention
status: active
raw_path: raw/Efficient Memory Management for Large Language Model Serving with PagedAttention.pdf
source_type: pdf
published: 2023-10
created: 2026-04-25
updated: 2026-04-27
---

# Summary

This paper argues that LLM serving throughput is often capped less by math kernels than by wasteful KV-cache memory management. It introduces PagedAttention and the `vLLM` serving engine to replace contiguous per-request KV allocation with fixed-size blocks, enabling larger batches, less fragmentation, and efficient sharing across sampling branches.

# Key Claims

- Existing serving systems waste substantial KV-cache memory through reserved space plus internal and external fragmentation.
- KV cache should be managed as fixed-size logical blocks mapped to physical blocks instead of one contiguous tensor per request.
- Paged KV storage makes prompt sharing, copy-on-write branching, and beam-search reuse much cheaper.
- Fine-grained iteration-level batching only reaches its potential when memory management also becomes fine-grained.
- The resulting system can improve throughput materially without changing model outputs.

# Why It Matters

This paper is one of the core building blocks behind modern LLM serving. It connects the abstract KV-cache problem to concrete scheduler behavior, batch size limits, and the practical economics of GPU memory.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [PagedAttention](../concepts/pagedattention.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)

# Open Questions

- The paper shows strong gains from better memory management, but the best trade-off between block size, transfer overhead, and kernel efficiency remains workload-sensitive.
- It does not resolve when prefill and decode should remain colocated versus fully disaggregated across machines.
