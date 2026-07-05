---
kind: source
title: "探秘Transformer系列之（27）--- MQA & GQA"
slug: cnblogs-transformer-series-27-mqa-and-gqa
source_ids:
  - raw-cnblogs-transformer-series-27-transformer-27-mqa-gqa
status: active
raw_path: raw/cnblogs-transformer-series/27-探秘Transformer系列之（27）--- MQA & GQA.md
source_type: markdown
parser: direct
published: 2025-04-14
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文从 MHA 出发，介绍 Multi-Query Attention 和 Grouped-Query Attention 的原理、实现和推理收益。核心是减少 K/V head 数以降低 KV cache 和 decode 带宽，同时尽量保留多 query head 的表达能力。

# Key Claims

- MQA 让所有 query heads 共享一组 K/V，大幅降低 KV cache，但可能牺牲质量。
- GQA 在 MHA 和 MQA 之间折中，把 query heads 分组，每组共享一组 K/V。
- MQA/GQA 的主要部署价值在 decode 阶段：更少 K/V head 意味着更小 cache 和更低 memory bandwidth。
- 训练或转换到 GQA/MQA 时需要关注质量保持、checkpoint 结构和 kernel 支持。

# Why It Matters

该文为 wiki 中 KV cache 优化提供了结构性 attention 变体的具体说明。

# Connections

- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- MQA/GQA 的质量影响依赖模型规模、训练 recipe 和任务；不能只按 cache 节省比例评估。
