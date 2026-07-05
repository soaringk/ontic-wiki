---
kind: source
title: "探秘Transformer系列之（28）--- DeepSeek MLA"
slug: cnblogs-transformer-series-28-deepseek-mla
source_ids:
  - raw-cnblogs-transformer-series-28-transformer-28-deepseek-mla
status: active
raw_path: raw/cnblogs-transformer-series/28-探秘Transformer系列之（28）--- DeepSeek MLA.md
source_type: markdown
parser: direct
published: 2025-04-17
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文深入讲解 DeepSeek MLA 的原理、核心要点、计算过程、代码、优化代码和权重转换。MLA 用低秩 latent 表示压缩 K/V cache，并在计算时恢复或重构所需 attention 表示。

# Key Claims

- MLA 把 K/V 缓存从完整 per-head 张量压缩到共享低维 latent，以显著降低每 token cache 维度。
- RoPE 与低秩压缩路径需要拆分处理，因为位置相关部分和可压缩内容的约束不同。
- MLA 用额外投影计算换取 cache 存储和带宽下降，适合 KV cache 成为瓶颈的长上下文和大 batch decode。
- 权重转换和 kernel 实现细节会决定 MLA 是否真正带来部署收益。

# Why It Matters

该文是 wiki 既有 Multi-head Latent Attention (MLA) 概念的强补充来源，细化了 DeepSeek 系列 KV cache 压缩路径。

# Connections

- Concept: [Multi-head Latent Attention (MLA)](../concepts/multi-head-latent-attention-mla.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)

# Open Questions

- MLA 的收益取决于实现是否把投影开销、cache 格式和 kernel 路径一起优化。
