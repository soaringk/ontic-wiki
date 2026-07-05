---
kind: source
title: "探秘Transformer系列之（33）--- DeepSeek MTP"
slug: cnblogs-transformer-series-33-deepseek-mtp
source_ids:
  - raw-cnblogs-transformer-series-33-transformer-33-deepseek-mtp
status: active
raw_path: raw/cnblogs-transformer-series/33-探秘Transformer系列之（33）--- DeepSeek MTP.md
source_type: markdown
parser: direct
published: 2025-05-17
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 EAGLE、Multi-token Prediction 和 DeepSeek MTP。MTP 在训练和推理中让模型显式预测多个未来 token，为 speculative/parallel decoding 提供更强候选或辅助训练信号。

# Key Claims

- Multi-token prediction 让模型不只预测下一个 token，而是学习多个未来偏移位置的 token。
- MTP 可以作为训练辅助目标，也可以为推理时多 token 候选生成提供结构基础。
- DeepSeek MTP 需要处理多 token 预测模块与主模型隐藏状态、loss 权重和推理验证的关系。
- 与 Medusa/EAGLE 类方案一样，收益取决于未来 token 预测准确率和验证成本。

# Why It Matters

该文把并行解码从推理技巧扩展到训练目标和模型结构层面，补充 Speculative Decoding 与 Parallel Decoding Variants 的联系。

# Connections

- Concept: [Parallel Decoding Variants](../concepts/parallel-decoding-variants.md)
- Concept: [Speculative Decoding](../concepts/speculative-decoding.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)

# Open Questions

- MTP 是否带来净收益，需要同时评估训练成本、模型质量、推理接受率和 serving 复杂度。
