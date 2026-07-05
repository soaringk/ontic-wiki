---
kind: source
title: "探秘Transformer系列之（11）--- 掩码"
slug: cnblogs-transformer-series-11-masks
source_ids:
  - raw-cnblogs-transformer-series-11-transformer-11
status: active
raw_path: raw/cnblogs-transformer-series/11-探秘Transformer系列之（11）--- 掩码.md
source_type: markdown
parser: direct
published: 2025-03-08
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文讲解 Transformer 中的 mask 需求、padding mask、sequence/causal mask、数据流和进阶 mask 用法。核心是区分填充位置不可见、未来 token 不可见、以及不同 attention 模块的信息边界。

# Key Claims

- Padding mask 防止模型把填充 token 当成真实内容参与 attention。
- Sequence/causal mask 使 decoder 训练时即使并行输入目标序列，也不能读取当前位置之后的未来 token。
- 不同 mask 通过 attention score 上的极小值或布尔选择影响 softmax 权重，本质上是在实现信息可见性约束。
- Mask 语义错误会导致训练泄漏、推理不一致或 padding 噪声进入表示。

# Why It Matters

该文强化了 wiki 对 mask 的边界意识：padding mask、causal mask 和 cross-attention 可见性不能被合并成一个模糊概念。

# Connections

- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

# Open Questions

- 现代推理框架中的 paged attention、prefix cache 和 chunked prefill 会引入更复杂的 runtime mask 组合。
