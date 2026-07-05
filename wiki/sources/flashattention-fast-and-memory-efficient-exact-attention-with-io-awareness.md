---
kind: source
title: "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
slug: flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness
source_ids:
  - raw-2205-14135v2
status: active
raw_path: raw/2205.14135v2.pdf
source_type: pdf
parser: mineru
published: 2022-06-24
created: 2026-07-06
updated: 2026-07-06
---

# Summary

This paper introduces FlashAttention, an exact attention algorithm that treats GPU memory movement as the central bottleneck. It tiles Q/K/V into SRAM, uses online softmax to combine partial blocks correctly, and recomputes attention blocks during the backward pass instead of storing the full attention matrix in HBM.

# Key Claims

- Standard attention is slow and memory-heavy because it materializes `S = QK^T` and `P = softmax(S)` in HBM, creating quadratic memory traffic in sequence length.
- FlashAttention keeps exact dense attention semantics while reducing extra memory to linear in sequence length.
- The algorithm is IO-aware: it optimizes reads and writes between HBM and on-chip SRAM, not just FLOP count.
- Tiling plus online softmax lets each block update the running row max, normalization sum, and output without needing the full row in memory.
- Backward recomputation avoids saving the `N x N` attention probabilities and can still be faster because it reduces HBM access.
- In experiments, FlashAttention improves BERT/GPT-2 training speed, allows longer context, and enables non-random Transformer results on Path-X; block-sparse FlashAttention extends the same primitive to sparse masks.

# Why It Matters

FlashAttention is the canonical example that exact Transformer attention can be made much faster by respecting GPU memory hierarchy. It preserves model quality better than many approximate attention methods because it does not approximate the dense attention operation.

# Connections

- Concept: [FlashAttention](../concepts/flashattention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [GPU Memory Hierarchy](../concepts/gpu-memory-hierarchy.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Topic: [CUDA Programming](../topics/cuda-programming.md)

# Open Questions

- The original implementation requires low-level CUDA work and is sensitive to GPU architecture; later versions address some of this through improved partitioning and Hopper-specific techniques.
