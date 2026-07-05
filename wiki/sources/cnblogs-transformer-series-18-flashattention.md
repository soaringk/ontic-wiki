---
kind: source
title: "探秘Transformer系列之（18）--- FlashAttention"
slug: cnblogs-transformer-series-18-flashattention
source_ids:
  - raw-cnblogs-transformer-series-18-transformer-18-flashattention
status: active
raw_path: raw/cnblogs-transformer-series/18-探秘Transformer系列之（18）--- FlashAttention.md
source_type: markdown
parser: direct
published: 2025-03-25
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 FlashAttention 的背景、注意力内存瓶颈、online softmax、tiling、FlashAttention V1 的 IO-aware 设计，以及计算量与显存占用分析。

# Key Claims

- 标准 attention 的主要工程问题不只是 FLOPs，而是中间注意力矩阵和 HBM 读写流量。
- Online softmax 允许分块计算 softmax 归一化结果，避免一次性物化完整 `n x n` attention matrix。
- FlashAttention 通过 block tiling 把 Q/K/V 分块搬入片上 SRAM，减少 HBM 往返并保持 exact attention 语义。
- FlashAttention 降低 activation memory 和内存流量，但 dense attention 的时间复杂度仍随序列长度二次增长。

# Why It Matters

该文补强 Attention Mechanism 和 serving 主题中“memory traffic 是 attention kernel 优化核心”的观点。

# Connections

- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [GPU Memory Hierarchy](../concepts/gpu-memory-hierarchy.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

# Open Questions

- 不同 FlashAttention 版本、GPU 架构和 framework integration 的性能边界需要实测。
