---
kind: source
title: "探秘Transformer系列之（24）--- KV Cache优化"
slug: cnblogs-transformer-series-24-kv-cache-optimization
source_ids:
  - raw-cnblogs-transformer-series-24-transformer-24-kv-cache
status: active
raw_path: raw/cnblogs-transformer-series/24-探秘Transformer系列之（24）--- KV Cache优化.md
source_type: markdown
parser: direct
published: 2025-04-08
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文从 KV Cache 资源公式和注意力特性出发，总结 KV Cache 优化方向：减少层数或 KV head 数、降低 head dimension、降低 dtype 位宽、压缩/量化、稀疏化、复用以及基于特性的系统优化。

# Key Claims

- KV cache 优化可以按公式项拆解：层数、KV head 数、head dimension、序列长度、batch、dtype 和并行分片。
- GQA/MQA/MLA 等结构性方法主要降低 KV head 或 KV 表示维度。
- Cache dtype 量化和压缩降低存储/带宽，但需要控制精度损失。
- Prefix/cache reuse、分页管理和调度策略会改变有效 cache 容量，属于系统层优化。

# Why It Matters

该文把 KV cache 从单一技术点转成可系统优化的空间，补充 wiki 中 context caching、quantization 和 serving capacity 的连接。

# Connections

- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- Concept: [PagedAttention](../concepts/pagedattention.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- 不同优化项可叠加但也可能互相影响；最终需要质量、吞吐、延迟和工程复杂度共同评估。
