---
kind: source
title: "探秘Transformer系列之（10）--- 自注意力"
slug: cnblogs-transformer-series-10-self-attention
source_ids:
  - raw-cnblogs-transformer-series-10-transformer-10
status: active
raw_path: raw/cnblogs-transformer-series/10-探秘Transformer系列之（10）--- 自注意力.md
source_type: markdown
parser: direct
published: 2025-03-05
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文深入讲解 self-attention 原理、矩阵实现、Q/K/V 投影、缩放点积、softmax、张量形状和若干优化方向。文章把自注意力看成让序列内部 token 彼此交互并生成上下文化表示的核心操作。

# Key Claims

- Self-attention 使用同一序列生成 Q、K、V，使每个 token 可以按相关性读取序列内其它 token 的信息。
- `QK^T / sqrt(d_k)` 的缩放点积避免分数方差随维度变大导致 softmax 过度饱和。
- 矩阵化实现把所有 token 的 Q/K/V 一次性计算出来，是训练并行性的关键。
- 优化注意力主要围绕减少中间矩阵、改善内存访问、融合 softmax 和降低 KV 读写成本展开。

# Why It Matters

该文为 Attention Mechanism 页面提供更细的公式与实现依据，也连接 FlashAttention、KV Cache、GQA/MQA/MLA 等后续优化。

# Connections

- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

# Open Questions

- 文中实现以教学清晰为主；生产 kernel 的真实性能需要结合具体硬件和框架。
