---
kind: source
title: "探秘Transformer系列之（3）---数据处理"
slug: cnblogs-transformer-series-03-data-processing
source_ids:
  - raw-cnblogs-transformer-series-03-transformer-3
status: active
raw_path: raw/cnblogs-transformer-series/03-探秘Transformer系列之（3）---数据处理.md
source_type: markdown
parser: direct
published: 2025-02-18
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文围绕 Harvard Annotated Transformer 的数据处理路径，介绍训练数据、验证数据、Multi30k 数据集、分词器、词表构建、数据加载器、batch 构造、padding 和 mask。文章也把 LLM 预训练数据治理放在更大背景中，强调数据质量、去重、隐私擦除、数据混合和 tokenization 的作用。

# Key Claims

- 数据和数据处理决定模型上限；预训练可被理解为从语料中提炼概率分布、降低任务域信息熵。
- 真实 LLM 数据流水线远比教学代码复杂，通常包括质量过滤、去重、隐私处理、分词和数据混合。
- 训练时需要把变长文本组织成 batch，并用 padding 和 attention mask 区分真实 token 与填充位置。
- Harvard 示例通过 Multi30k、spaCy 分词器、torchtext 词表和 dataloader 展示了可运行的端到端数据路径。

# Why It Matters

该文补足 Transformer 架构之前的数据入口：token、vocabulary、padding、batch 和 mask 不是外围工程细节，而是模型张量形状和训练正确性的前置条件。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)

# Open Questions

- 文中教学代码不代表生产级预训练数据管线；质量过滤和数据混合策略需要专门来源支撑。
