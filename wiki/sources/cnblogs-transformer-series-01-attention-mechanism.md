---
kind: source
title: "探秘Transformer系列之（1）：注意力机制"
slug: cnblogs-transformer-series-01-attention-mechanism
source_ids:
  - raw-cnblogs-transformer-series-01-transformer-1
status: active
raw_path: raw/cnblogs-transformer-series/01-探秘Transformer系列之（1）：注意力机制.md
source_type: markdown
parser: direct
published: 2025-02-09
created: 2026-07-04
updated: 2026-07-04
---

# Summary

罗西的中文 Transformer 系列开篇文章，从 Seq2Seq、文本生成、自回归、隐变量自回归、Encoder-Decoder、CNN/RNN 的长依赖和对齐困难，逐步引出注意力机制。文章把注意力解释为让模型按上下文动态分配信息资源的机制，并梳理了从早期 Encoder-Decoder Attention 到 Self-Attention、QKV-Attention、多头注意力的演进。

# Key Claims

- 序列建模的核心问题是如何压缩并保留长序列上下文中的关系。
- CNN 依赖局部卷积和堆叠扩大感受野，RNN 依赖隐状态递归传递信息，两者都容易在长依赖、对齐、并行训练上受限。
- Attention 通过按 query 与 key 的相关性为 value 加权，让解码当前位置可以选择性聚合输入序列信息。
- Q/K/V 视角把“查什么、被查什么、取回什么”分离，是后续 self-attention 和 multi-head attention 的抽象基础。

# Why It Matters

该文为 wiki 中 Transformer、Attention、Autoregressive Generation 的背景材料补足了从 RNN/CNN 到注意力机制的动机链条，特别适合解释为什么 Transformer 不是单纯替换网络层，而是改变了序列中信息交换的路径长度。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)

# Open Questions

- 文章采用教学性反推叙事；涉及历史归因时应以原始论文为准。
