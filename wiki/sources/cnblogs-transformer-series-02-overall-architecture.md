---
kind: source
title: "探秘Transformer系列之（2）---总体架构"
slug: cnblogs-transformer-series-02-overall-architecture
source_ids:
  - raw-cnblogs-transformer-series-02-transformer-2
status: active
raw_path: raw/cnblogs-transformer-series/02-探秘Transformer系列之（2）---总体架构.md
source_type: markdown
parser: direct
published: 2025-02-15
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文以 `Attention Is All You Need` 和 Harvard Annotated Transformer 为主线，讲解 Transformer 文本生成流程、原始 Encoder-Decoder 结构、三类注意力模块、构建函数、输入层、Transformer Layer、概率输出以及若干解释性研究。

# Key Claims

- 文本生成流程可拆成 tokenize、编码、embedding、位置编码、注意力计算、logits、softmax/采样和循环生成。
- 原始 Transformer 由输入模块、Encoder 栈、Decoder 栈、输出模块组成；Encoder/Decoder layer 是重复堆叠的基本单元。
- 全局自注意力、因果掩码自注意力、交叉注意力使用同一注意力计算模板，但 Q/K/V 来源和可见信息边界不同。
- MLP/FFN、残差连接、LayerNorm 等结构不是附属细节；它们防止秩坍塌、稳定深层网络，并补足 attention 之外的非线性加工。

# Why It Matters

该文把 Transformer 的端到端运行流程与代码构建边界对齐，有助于 wiki 把抽象架构、mask 语义、serving 中 prefill/decode 的执行路径放在同一张图里理解。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)
- Concept: [Token Sampling Strategies](../concepts/token-sampling-strategies.md)

# Open Questions

- 文中以经典 Encoder-Decoder 翻译模型为主；现代 decoder-only LLM 的 serving 细节需要结合后续 KV Cache 与推理优化文章。
