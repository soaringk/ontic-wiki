---
kind: source
title: "探秘Transformer系列之（15）--- 采样和输出"
slug: cnblogs-transformer-series-15-sampling-and-output
source_ids:
  - raw-cnblogs-transformer-series-15-transformer-15
status: active
raw_path: raw/cnblogs-transformer-series/15-探秘Transformer系列之（15）--- 采样和输出.md
source_type: markdown
parser: direct
published: 2025-03-18
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文讲解 Generator/LM head、logits、softmax、采样策略、采样参数、logits 分析和权重共享。它把模型最后一步输出解释为从隐藏状态到词表概率分布，再按策略选择下一个 token。

# Key Claims

- Generator/LM head 把 decoder 输出投影到词表维度，得到每个 token 的 logits。
- Greedy、temperature、Top-K、Top-P 等采样策略改变输出多样性和风险，但不改变底层模型架构。
- Temperature 调整 logits 分布尖锐程度；Top-K/Top-P 限制候选集合以避免低概率尾部噪声。
- Input embedding 与 output projection 权重共享可减少参数并让输入/输出 token 空间保持一致。

# Why It Matters

该文是 Token Sampling Strategies 概念的直接中文来源，也把采样与 serving 中的 decode loop、质量/延迟权衡连接起来。

# Connections

- Concept: [Token Sampling Strategies](../concepts/token-sampling-strategies.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Concept: [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)

# Open Questions

- 采样参数最佳值是任务和产品策略问题，不能由单篇架构教程固定。
