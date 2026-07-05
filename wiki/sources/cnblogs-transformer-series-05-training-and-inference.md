---
kind: source
title: "探秘Transformer系列之（5）--- 训练&推理"
slug: cnblogs-transformer-series-05-training-and-inference
source_ids:
  - raw-cnblogs-transformer-series-05-transformer-5
status: active
raw_path: raw/cnblogs-transformer-series/05-探秘Transformer系列之（5）--- 训练&推理.md
source_type: markdown
parser: direct
published: 2025-02-22
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文解释 Transformer 训练与推理的差异：训练阶段通过 teacher forcing、目标序列右移、mask、dropout、交叉熵/标签平滑和优化器并行学习；推理阶段只给输入序列，解码器自回归地产生下一个 token 并把输出回填到下一步输入。

# Key Claims

- 自回归模型推理必须串行生成，但训练可以用 teacher forcing 和 causal mask 并行计算所有位置的 next-token loss。
- Dropout 在训练时作为正则化和近似集成机制，在推理时通常关闭；大模型是否需要 dropout 与规模、数据、多种正则化机制有关。
- Generator/LM head 把隐藏状态映射到词表维度 logits，交叉熵优化的是预测分布与目标 token 分布之间的差异。
- 训练和推理共享模型权重，但输入组织、mask 行为、是否使用真实目标序列，以及是否启用随机正则化都不同。

# Why It Matters

该文把训练并行性和推理串行性的差异讲清楚，为后续 KV Cache、speculative decoding、serving latency 指标提供了直接背景。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Concept: [Token Sampling Strategies](../concepts/token-sampling-strategies.md)

# Open Questions

- 文章使用教学训练循环；现代大模型训练的分布式并行、优化器状态和混合精度细节需要其他资料补充。
