---
kind: source
title: "3.9 Tokenization与词嵌入"
slug: tokenization-and-word-embedding
source_ids:
  - raw-aiinfraguide-3-9-tokenization
status: active
raw_path: raw/AIInfraGuide/3.9 Tokenization与词嵌入.md
source_type: markdown
parser: direct
published: 2026-04-24
created: 2026-06-11
updated: 2026-06-11
---

# Summary

这篇文章解释文本进入 Transformer 前的两步转换：Tokenization 把文本切成 token 并映射到 token ID，Embedding 把 token ID 查表成稠密向量；它同时讨论 BPE、中文 tokenization、one-hot 的缺陷、词嵌入几何和位置编码缺口。

# Key Claims

- Token 是 Transformer 处理文本的基本单元，现代大模型通常使用子词切分而不是纯字符级或词级切分。
- BPE 从字符/字节出发合并高频组合，能覆盖常见词，并用子词拼出生僻词以避免 OOV。
- 中文没有空格边界，中文友好模型通常需要更大的词表或更多中文词组 token，以改善生成效率和 token 利用率。
- One-hot 编码维度大且 token 之间完全正交，既低效又不能表达语义相似性。
- Embedding 是可学习查找表 `V x d_model`，把 token 映射到连续语义空间，Embedding 参数量随词表和模型维度线性增长。
- 静态 embedding 不携带词序，且不能独立解决上下文消歧；顺序由位置编码注入，动态语义由 Self-Attention 层层更新。
- Embedding 和 LM Head 可通过 weight tying 共享权重，节省一个 `V x d_model` 矩阵。

# Why It Matters

Tokenization 和 Embedding 决定模型实际看到的离散输入、词表成本、多语言 token 效率、embedding 参数量，以及输入层到 Decoder Block 的边界。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)
- Concept: [Positional Encoding](../concepts/positional-encoding.md)

# Source Notes

- Canonical raw capture: `raw/AIInfraGuide/3.9 Tokenization与词嵌入.md`.

# Open Questions

- 具体 tokenizer 的中英文效率、特殊 token 行为和上下文长度消耗需要以实际 tokenizer 编码结果验证。
