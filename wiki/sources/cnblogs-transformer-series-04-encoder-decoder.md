---
kind: source
title: "探秘Transformer系列之（4）--- 编码器 & 解码器"
slug: cnblogs-transformer-series-04-encoder-decoder
source_ids:
  - raw-cnblogs-transformer-series-04-transformer-4
status: active
raw_path: raw/cnblogs-transformer-series/04-探秘Transformer系列之（4）--- 编码器 & 解码器.md
source_type: markdown
parser: direct
published: 2025-02-20
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文细化 Transformer Encoder、Decoder、Cross-Attention 和 Decoder-only 变体。它从机器翻译前向计算出发，解释 Encoder 并行处理源序列、Decoder 自回归循环生成目标序列，以及交叉注意力如何在两个序列之间传递信息。

# Key Claims

- Encoder layer 由 self-attention、残差连接、LayerNorm、FFN 组成，输入输出维度保持一致，便于层叠。
- Decoder layer 在 masked self-attention 和 FFN 之间增加 cross-attention，使目标序列位置可以读取 Encoder 输出 memory。
- Cross-attention 的 Q 来自 decoder，K/V 来自 encoder，是传统 seq2seq 对齐机制在 Transformer 中的实现。
- Decoder-only LLM 删除 encoder 和 cross-attention，仅保留因果 self-attention 路径，形成现代生成式 LLM 的主流结构。

# Why It Matters

该文清楚区分了 Encoder-Decoder 与 Decoder-only 的结构边界，是理解为什么现代 LLM serving 主要关注 causal attention、KV cache 和 decode loop 的桥梁。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Concept: [Transformer Normalization and Residuals](../concepts/transformer-normalization-and-residuals.md)

# Open Questions

- 文章比较的是结构路径；不同模型族的实际能力差异还依赖训练目标、数据和规模。
