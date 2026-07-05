---
kind: source
title: "探秘Transformer系列之（9）--- 位置编码分类"
slug: cnblogs-transformer-series-09-positional-encoding-taxonomy
source_ids:
  - raw-cnblogs-transformer-series-09-transformer-9
status: active
raw_path: raw/cnblogs-transformer-series/09-探秘Transformer系列之（9）--- 位置编码分类.md
source_type: markdown
parser: direct
published: 2025-03-03
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文按绝对位置编码与相对位置编码分类，比较不同位置编码方案对顺序、距离、可外推性和注意力计算的影响。

# Key Claims

- 绝对位置编码直接为每个位置提供编号或向量，简单但外推和相对距离表达受限。
- 相对位置编码把位置关系注入 token 对之间的 attention 计算，更贴近语言中“相对距离”影响关系建模的需求。
- 位置编码分类应关注信号注入位置：embedding 加法、attention bias、Q/K 旋转或其它 score-level 修改。
- RoPE 之所以重要，是因为它用旋转方式把相对位置信息折进 Q/K 点积。

# Why It Matters

该文把位置编码从“一个输入向量”扩展为多种信息注入策略，有助于理解 RoPE、ALiBi 和长上下文扩展方案的共同设计空间。

# Connections

- Concept: [Positional Encoding](../concepts/positional-encoding.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

# Open Questions

- 位置编码分类是结构视角；实际可用上下文长度还需要实验证据。
