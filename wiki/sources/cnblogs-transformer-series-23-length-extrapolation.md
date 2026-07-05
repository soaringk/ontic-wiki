---
kind: source
title: "探秘Transformer系列之（23）--- 长度外推"
slug: cnblogs-transformer-series-23-length-extrapolation
source_ids:
  - raw-cnblogs-transformer-series-23-transformer-23
status: active
raw_path: raw/cnblogs-transformer-series/23-探秘Transformer系列之（23）--- 长度外推.md
source_type: markdown
parser: direct
published: 2025-04-05
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍长度外推背景、位置编码与外推关系、RoPE 外推问题，以及基础和进阶 RoPE scaling 方案。重点是训练上下文长度之外推理时，位置分布和注意力模式发生偏移导致质量下降。

# Key Claims

- 长度外推是模型在超过训练长度的序列上保持可用能力的问题，不等同于简单扩大 KV cache 容量。
- 位置编码决定模型看到的位置信号分布，训练外位置可能导致频率、距离和 attention score 分布失配。
- RoPE 外推方案通常通过位置插值、频率缩放或分段缩放缓解训练长度外的位置失配。
- 外推方案会影响长上下文质量、短上下文保持、KV cache 位置一致性和 serving 支持的上下文窗口。

# Why It Matters

该文把长上下文从内存问题扩展为位置泛化问题，连接 Positional Encoding、KV Cache 和 LLM deployment capacity planning。

# Connections

- Concept: [Long Context Extrapolation](../concepts/long-context-extrapolation.md)
- Concept: [Positional Encoding](../concepts/positional-encoding.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- 外推后的实际能力需要长文任务评测；支持更长上下文窗口不保证有效利用全部上下文。
