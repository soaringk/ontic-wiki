---
kind: source
title: "探秘Transformer系列之（7）--- embedding"
slug: cnblogs-transformer-series-07-embedding
source_ids:
  - raw-cnblogs-transformer-series-07-transformer-7-embedding
status: active
raw_path: raw/cnblogs-transformer-series/07-探秘Transformer系列之（7）--- embedding.md
source_type: markdown
parser: direct
published: 2025-02-27
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文讲解 embedding 的演进思路、Transformer 嵌入层实现和文本嵌入应用。它把 token ID 到向量的转换放在从 one-hot、分布式表示、词向量、上下文化表示到现代文本 embedding 的连续谱中理解。

# Key Claims

- Embedding 层把离散 token ID 映射为稠密向量，是 Transformer 能进行连续数值计算的入口。
- 词向量不仅是编码格式，也承载语义相似性、上下文关系和后续 attention 可加工的信息。
- Transformer 中 token embedding 通常与位置编码相加后进入 block；输出侧也常与 LM head 权重共享以降低参数量并约束输入输出空间一致。
- 文本嵌入用于检索、聚类、分类和语义匹配，但它和生成模型内部 token embedding 的用途不同。

# Why It Matters

该文把 tokenization 与后续向量化连接起来，补充了 vocabulary size、embedding table、LM head 和 weight tying 对参数量与部署内存的影响。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)

# Open Questions

- 文本 embedding 的检索用途应与向量数据库资料结合阅读，避免和生成模型内部 embedding 混为一谈。
