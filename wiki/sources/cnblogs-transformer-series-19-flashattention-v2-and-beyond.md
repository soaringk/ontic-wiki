---
kind: source
title: "探秘Transformer系列之（19）----FlashAttention V2 及升级版本"
slug: cnblogs-transformer-series-19-flashattention-v2-and-beyond
source_ids:
  - raw-cnblogs-transformer-series-19-transformer-19-flashattention-v2
status: active
raw_path: raw/cnblogs-transformer-series/19-探秘Transformer系列之（19）----FlashAttention V2 及升级版本.md
source_type: markdown
parser: direct
published: 2025-03-28
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文延续 FlashAttention，介绍 FlashAttention V2、Flash-Decoding、Flash-Mask 和 FlashAttention-3。重点从 IO 优化扩展到更高并行度、更少非矩阵乘法开销、更适合 decode 的 kernel 组织和新硬件特性利用。

# Key Claims

- FlashAttention V2 通过减少非 matmul FLOPs、调整 work partition 和改善 warp/block 级并行，提高 GPU 利用率。
- Prefill 和 decode 的 kernel 需求不同；Flash-Decoding 针对单 token query、多历史 K/V 的 decode 场景提升并行度。
- Flash-Mask 等变体说明 mask 处理也会影响 attention kernel 的实用性能。
- FlashAttention-3 继续围绕 Hopper 等新硬件能力优化异步执行和低精度路径。

# Why It Matters

该文把 FlashAttention 从一个算法点扩展为一组随硬件和 serving phase 演化的 kernel 设计，有助于理解 prefill/decode 性能差异。

# Connections

- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Model Bandwidth Utilization](../concepts/model-bandwidth-utilization.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- 版本名称不能替代 benchmark；需要按序列长度、batch、GPU 架构和框架集成实测。
