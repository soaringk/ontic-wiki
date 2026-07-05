---
kind: source
title: "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning"
slug: flashattention-2-faster-attention-with-better-parallelism-and-work-partitioning
source_ids:
  - raw-2307-08691v1
status: active
raw_path: raw/2307.08691v1.pdf
source_type: pdf
parser: mineru
published: 2023-07-18
created: 2026-07-06
updated: 2026-07-06
---

# Summary

FlashAttention-2 keeps the exact tiled-attention idea but improves GPU utilization through better algorithmic bookkeeping, sequence-parallel work decomposition, and warp-level work partitioning. It targets the gap between FlashAttention and optimized GEMM throughput on A100-class GPUs.

# Key Claims

- FlashAttention is IO-efficient but still underutilizes GPU compute compared with optimized matrix multiplication.
- FlashAttention-2 reduces non-matmul FLOPs by maintaining an unscaled output accumulator and storing row-wise logsumexp for backward instead of separate max and sum statistics.
- It parallelizes attention over sequence blocks in addition to batch and heads, improving occupancy when long sequences force small batch sizes.
- It changes warp partitioning from split-K-style communication to splitting Q across warps, reducing shared-memory reads/writes in the forward pass.
- The implementation supports causal masks, MQA, and GQA without changing exact attention semantics.
- Experiments report roughly 1.7-3.0x speedup over FlashAttention, up to 230 TFLOPs/s on A100 attention benchmarks, and up to 225 TFLOPs/s per A100 in GPT-style training.

# Why It Matters

FlashAttention-2 shows that once memory IO is controlled, the next bottleneck is work partitioning: enough parallel blocks must be exposed, and intra-block communication must be minimized so Tensor Cores stay busy.

# Connections

- Concept: [FlashAttention](../concepts/flashattention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [CUDA Thread Hierarchy](../concepts/cuda-thread-hierarchy.md)
- Concept: [GPU Memory Hierarchy](../concepts/gpu-memory-hierarchy.md)
- Topic: [CUDA Programming](../topics/cuda-programming.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

# Open Questions

- Block-size and head-dimension choices remain tuning-sensitive, and the paper explicitly points toward future autotuning and hardware-specific implementations.
