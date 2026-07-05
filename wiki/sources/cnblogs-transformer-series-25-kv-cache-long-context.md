---
kind: source
title: "探秘Transformer系列之（25）--- KV Cache优化之处理长文本序列"
slug: cnblogs-transformer-series-25-kv-cache-long-context
source_ids:
  - raw-cnblogs-transformer-series-25-transformer-25-kv-cache
status: active
raw_path: raw/cnblogs-transformer-series/25-探秘Transformer系列之（25）--- KV Cache优化之处理长文本序列.md
source_type: markdown
parser: direct
published: 2025-04-10
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文聚焦长文本序列下的 KV Cache 优化，讨论优化依据、稀疏化、复用和基于检索的方案。它把长上下文成本拆成“哪些历史 token 必须保留、哪些可以压缩/丢弃、哪些可按需检索”。

# Key Claims

- 长上下文下，KV cache 随序列长度线性增长，attention 读历史 K/V 的带宽压力也同步增长。
- Sparse/sliding-window/selected attention 通过减少可见历史 token 降低存储和计算。
- Prefix reuse 和 context caching 适合重复提示词、共享系统 prompt 和多轮会话中的公共前缀。
- Retrieval-based KV 或外部检索方案尝试把“全部保留上下文”转化为“按需取回相关信息”。

# Why It Matters

该文扩展 wiki 对 KV cache 的长上下文视角：容量规划不能只增加显存，还要考虑稀疏、复用和检索式上下文管理。

# Connections

- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- Concept: [Long Context Extrapolation](../concepts/long-context-extrapolation.md)

# Open Questions

- 稀疏/检索式方案可能改变模型可见信息边界；质量风险需要任务级验证。
