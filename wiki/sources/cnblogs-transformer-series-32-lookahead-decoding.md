---
kind: source
title: "探秘Transformer系列之（32）--- Lookahead Decoding"
slug: cnblogs-transformer-series-32-lookahead-decoding
source_ids:
  - raw-cnblogs-transformer-series-32-transformer-32-lookahead-decoding
status: active
raw_path: raw/cnblogs-transformer-series/32-探秘Transformer系列之（32）--- Lookahead Decoding.md
source_type: markdown
parser: direct
published: 2025-05-10
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 Lookahead Decoding，从 Jacobi decoding 动机出发，讲解 2D window、n-gram pool、guess set size、lookahead 分支、verification 分支和 llama.cpp 实现路径。

# Key Claims

- Lookahead decoding 尝试在不训练额外模型的情况下并行探索未来 token 候选。
- 2D window 和 n-gram pool 用于组织候选片段，verification 分支验证候选能否被原模型接受。
- 该方法利用语言中 n-gram/局部片段重复性，让模型在单步 decode 外获得额外可验证候选。
- 收益依赖候选命中率、verification 开销和实现对 KV/cache/mask 的支持。

# Why It Matters

该文补充 Parallel Decoding Variants：它代表“不额外训练 draft model 或 heads”的推理时并行候选生成路径。

# Connections

- Concept: [Parallel Decoding Variants](../concepts/parallel-decoding-variants.md)
- Concept: [Speculative Decoding](../concepts/speculative-decoding.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)

# Open Questions

- Lookahead 的实际加速高度依赖文本分布和 engine 实现，不能直接推广到所有 workload。
