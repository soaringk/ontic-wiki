---
kind: source
title: "探秘Transformer系列之（13）--- FFN"
slug: cnblogs-transformer-series-13-ffn
source_ids:
  - raw-cnblogs-transformer-series-13-transformer-13-ffn
status: active
raw_path: raw/cnblogs-transformer-series/13-探秘Transformer系列之（13）--- FFN.md
source_type: markdown
parser: direct
published: 2025-03-14
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文讲解 Transformer FFN 的网络结构、实现、作用、知识利用和演进。它把 FFN 解释为每个 token 独立执行的非线性特征变换，也是 dense Transformer block 中参数量和知识存储的重要来源。

# Key Claims

- 标准 FFN 通常是 `d_model -> d_ff -> d_model` 的两层线性结构，中间加激活函数和 dropout。
- Attention 负责 token 间信息交换，FFN 负责对每个 token 的表示进行独立非线性加工。
- FFN 往往占 dense Transformer 参数的大部分，因此也是模型容量、知识记忆和压缩优化的重要对象。
- SwiGLU、MoE、低秩/稀疏化等方案都可视作对 FFN 路径的容量和计算效率重设计。

# Why It Matters

该文加深了 wiki 对“attention 不是全部”的表述：LLM serving 的参数内存、GEMM 负载、MoE 专家化和模型压缩都强依赖 FFN 结构。

# Connections

- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

# Open Questions

- FFN 中知识存储的解释仍是研究话题，应和 mechanistic interpretability 证据区分开。
