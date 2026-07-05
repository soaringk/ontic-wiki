---
kind: source
title: "探秘Transformer系列之（20）--- KV Cache"
slug: cnblogs-transformer-series-20-kv-cache
source_ids:
  - raw-cnblogs-transformer-series-20-transformer-20-kv-cache
status: active
raw_path: raw/cnblogs-transformer-series/20-探秘Transformer系列之（20）--- KV Cache.md
source_type: markdown
parser: direct
published: 2025-03-30
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文解释自回归推理为何会重复计算历史 token，以及 KV Cache 如何缓存历史 K/V 来把每步 decode 变成“新 query 读取历史 K/V”。文章覆盖实现路径、资源占用和性能收益。

# Key Claims

- 无 cache 的自回归推理每一步都重算完整前缀，历史 token 的 K/V 被反复生成。
- KV Cache 在 prefill 阶段写入 prompt 的 K/V，在 decode 阶段每步只追加新 token 的 K/V 并读取历史 K/V。
- Cache 大小与层数、KV head 数、head dimension、序列长度、batch、dtype 和并行切分相关。
- KV Cache 用空间换时间，降低重复计算但增加显存压力和 cache 管理复杂度。

# Why It Matters

该文是 wiki 中 KV Cache in LLM Serving 的直接中文教程来源，连接 autoregressive generation、TTFT/TPOT 和容量规划。

# Connections

- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- KV cache 的实际布局、分页、共享和迁移策略取决于 serving engine。
