---
kind: source
title: "探秘Transformer系列之（12）--- 多头自注意力"
slug: cnblogs-transformer-series-12-multi-head-self-attention
source_ids:
  - raw-cnblogs-transformer-series-12-transformer-12
status: active
raw_path: raw/cnblogs-transformer-series/12-探秘Transformer系列之（12）--- 多头自注意力.md
source_type: markdown
parser: direct
published: 2025-03-11
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 multi-head self-attention 的研究背景、原理、实现和改进。它解释了为什么把注意力拆成多个 head 可以让模型在不同子空间学习不同关系，并展示了投影、split heads、并行 attention、concat 和 output projection 的实现形状。

# Key Claims

- 多头注意力不是简单重复，而是把模型维度拆到多个关系子空间中并行建模。
- 每个 head 都有独立 Q/K/V 投影；head 输出拼接后通过输出投影回到 `d_model`。
- Head 维度、head 数量和 Q/K/V 形状直接影响参数量、计算量、tensor parallel 切分和 KV cache 大小。
- MQA/GQA 等改进可以看作在保留多 query head 的同时减少 K/V head 以降低推理内存和带宽压力。

# Why It Matters

该文把多头注意力从概念解释推进到实现张量形状，为 wiki 中 parallelism、KV cache、MQA/GQA/MLA 的联系提供依据。

# Connections

- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- Head 的语义解释通常是后验分析；不能假设每个 head 都稳定对应人类可命名功能。
