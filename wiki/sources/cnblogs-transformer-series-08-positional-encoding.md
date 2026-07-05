---
kind: source
title: "探秘Transformer系列之（8）--- 位置编码"
slug: cnblogs-transformer-series-08-positional-encoding
source_ids:
  - raw-cnblogs-transformer-series-08-transformer-8
status: active
raw_path: raw/cnblogs-transformer-series/08-探秘Transformer系列之（8）--- 位置编码.md
source_type: markdown
parser: direct
published: 2025-03-01
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文从 self-attention 的顺序盲点出发，介绍位置编码问题、编码方案演化、正弦/余弦位置编码的构造与性质，以及 NoPE 等不显式加入位置编码的探索。

# Key Claims

- Self-attention 本身对输入顺序不敏感，必须通过某种机制把位置信息注入表示或注意力分数。
- 原始 Transformer 的三角函数位置编码使用不同频率的 sin/cos 维度，为模型提供绝对位置和相对距离可推导的信号。
- 位置编码既可加到 token embedding 上，也可通过注意力打分或 Q/K 变换引入；不同方案影响长度外推和 kernel 实现。
- NoPE 等方案尝试减少显式位置编码，但仍需要解释模型如何获得顺序信息。

# Why It Matters

该文补足位置编码的基础动机，为 RoPE、ALiBi、长度外推、KV cache 中位置一致性和长上下文 serving 讨论提供背景。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Positional Encoding](../concepts/positional-encoding.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)

# Open Questions

- 长上下文能力不能只由位置编码形式决定，还取决于训练长度、数据分布和推理时缩放策略。
