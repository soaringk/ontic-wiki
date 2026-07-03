---
kind: source
title: Self-attention Does Not Need O(n^2) Memory
slug: self-attention-does-not-need-o-n2-memory
source_ids:
  - raw-2112-05682v3
status: active
raw_path: raw/2112.05682v3.pdf
source_type: pdf
parser: mineru
published: 2021-12-10
created: 2026-06-30
updated: 2026-06-30
---

# Summary

Rabe and Staats show that exact dot-product attention does not inherently require materializing the full attention matrix. By accumulating softmax numerator and denominator terms incrementally, and by tracking the running maximum for numerical stability, attention can be computed with much lower activation memory while preserving the same function.

# Key Claims

- Single-query attention can be computed with constant memory in sequence length by delaying softmax normalization until the final division.
- Self-attention can be extended to logarithmic memory in the abstract model by processing queries sequentially, although outputs still scale linearly and time remains quadratic.
- A practical accelerator implementation chunks queries and key/value blocks, giving an exact attention implementation with roughly `O(sqrt(n))` overhead memory.
- Numerical stability requires an online-softmax-style running maximum and rescaling of accumulated weights and values.
- Differentiation remains memory-efficient by checkpointing chunk summaries and recomputing them during backpropagation rather than storing the full attention matrix.
- On TPUv3, the implementation reduced self-attention memory overhead at sequence length 16,384 by 59x for inference and 32x for differentiation, with modest runtime differences in the measured settings.

# Why It Matters

The paper separates attention's quadratic time cost from its commonly assumed quadratic memory cost. That distinction matters for long-context Transformers and for later exact-attention kernels such as FlashAttention: many practical wins come from avoiding the materialized attention matrix, not from changing the model's attention semantics.

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)

# Open Questions

- The algorithm preserves exact dense attention but does not reduce quadratic compute, so it does not by itself solve very long-context throughput.
- The best chunk sizes are hardware- and workload-dependent; the paper explicitly trades the lowest theoretical memory for a simpler practical implementation.
