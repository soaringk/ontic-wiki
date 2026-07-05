---
kind: source
title: "探秘Transformer系列之（6）--- token"
slug: cnblogs-transformer-series-06-token
source_ids:
  - raw-cnblogs-transformer-series-06-transformer-6-token
status: active
raw_path: raw/cnblogs-transformer-series/06-探秘Transformer系列之（6）--- token.md
source_type: markdown
parser: direct
published: 2025-02-24
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文系统介绍 token、tokenizer、词表、规范化、预分词、模型处理、后处理、BPE、WordPiece、Unigram、SentencePiece 以及多语言/代码场景中的分词器演进。文章把文本到模型输入的转换拆成分词、索引化和后续 embedding 化。

# Key Claims

- Tokenizer 的本质是把字符串映射到整数 token ID，词表定义了模型实际能直接处理的离散符号空间。
- 分词流程通常包括 normalization、pre-tokenization、tokenization model、post-processing；特殊 token、padding 和 attention mask 都属于模型输入契约的一部分。
- BPE 从字符级符号开始迭代合并高频相邻片段，平衡词表大小、未知词处理和压缩效率。
- 分词器选择会影响多语言压缩率、代码建模、token 边界偏差和最终推理成本。

# Why It Matters

该文强化了 wiki 中“tokenization 不是前处理小事”的观点：词表大小和 token 切分会影响 embedding/LM-head 参数、上下文长度利用率、吞吐和跨语言表现。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)

# Open Questions

- 具体分词器优劣需要结合目标语料和模型训练目标评估，不能只依据算法名称判断。
