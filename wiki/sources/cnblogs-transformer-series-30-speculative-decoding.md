---
kind: source
title: "探秘Transformer系列之（30）--- 投机解码"
slug: cnblogs-transformer-series-30-speculative-decoding
source_ids:
  - raw-cnblogs-transformer-series-30-transformer-30
status: active
raw_path: raw/cnblogs-transformer-series/30-探秘Transformer系列之（30）--- 投机解码.md
source_type: markdown
parser: direct
published: 2025-04-23
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 speculative decoding 的背景、定义、历史、blockwise parallel decoding、原理、算法、实现和 token tree verification。核心是用 draft model 或并行候选生成多个 token，再由 target model 一次性验证，以减少串行 decode 步数。

# Key Claims

- 投机解码利用小模型/草稿路径快速提出候选 token，目标模型并行验证候选，接受前缀后减少目标模型调用次数。
- 正确的 rejection sampling 可以在加速的同时保持目标模型输出分布不变。
- 速度收益取决于 draft model 成本、接受率、候选长度、batching 和验证开销。
- Token tree verification 把候选组织成树，允许一次目标模型前向验证多个分支。

# Why It Matters

该文补强 Speculative Decoding 概念，扩展了 serving acceleration 从单一论文到 blockwise 和 tree verification 实现空间。

# Connections

- Concept: [Speculative Decoding](../concepts/speculative-decoding.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- 投机解码不是无条件加速；低接受率或服务端 batch 干扰可能抵消收益。
