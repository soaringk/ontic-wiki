---
kind: source
title: "探秘Transformer系列之（31）--- Medusa"
slug: cnblogs-transformer-series-31-medusa
source_ids:
  - raw-cnblogs-transformer-series-31-transformer-31-medusa
status: active
raw_path: raw/cnblogs-transformer-series/31-探秘Transformer系列之（31）--- Medusa.md
source_type: markdown
parser: direct
published: 2025-04-28
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 Medusa 的原理、设计核心、tree verification、训练和 decoding。Medusa 在 base LLM 后增加多个预测 head，用单模型多头方式提出未来 token 候选，再通过树验证接受多个 token。

# Key Claims

- Medusa 不依赖独立 draft model，而是在主模型上添加多个 decoding heads 预测未来位置候选。
- 多 head 候选需要 tree attention/tree verification 来一次性验证多分支 token 序列。
- Medusa 训练要让附加 heads 学会预测不同未来偏移，同时保持 base model 能力。
- 加速收益依赖候选质量、树结构、验证开销和最终接受 token 数。

# Why It Matters

该文扩展 Speculative Decoding 页面：并行解码不一定必须是双模型 draft-target 结构，也可以是附加 head 的单模型候选生成。

# Connections

- Concept: [Speculative Decoding](../concepts/speculative-decoding.md)
- Concept: [Parallel Decoding Variants](../concepts/parallel-decoding-variants.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)

# Open Questions

- 附加 heads 的训练和部署改造成本需要和外部 draft model 方案比较。
