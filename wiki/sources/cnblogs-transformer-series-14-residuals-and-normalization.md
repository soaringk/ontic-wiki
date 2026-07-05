---
kind: source
title: "探秘Transformer系列之（14）--- 残差网络和归一化"
slug: cnblogs-transformer-series-14-residuals-and-normalization
source_ids:
  - raw-cnblogs-transformer-series-14-transformer-14
status: active
raw_path: raw/cnblogs-transformer-series/14-探秘Transformer系列之（14）--- 残差网络和归一化.md
source_type: markdown
parser: direct
published: 2025-03-16
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍残差连接、归一化、BatchNorm、LayerNorm、Pre-Norm/Post-Norm、RMSNorm、DeepNorm 等机制，并结合 Transformer 实现解释它们在深层网络训练稳定性中的作用。

# Key Claims

- 残差连接给深层网络提供近似恒等路径，缓解梯度消失并允许层只学习增量变换。
- BatchNorm 更适合 batch 维统计稳定的场景；LayerNorm 在序列模型中按单样本隐藏维归一化，更适配变长文本。
- Pre-Norm 通常比 Post-Norm 更利于深层 Transformer 训练稳定，但可能影响表示尺度和最终性能权衡。
- RMSNorm 去掉均值中心化，只保留均方根尺度控制，是现代 LLM 中常见的轻量归一化选择。

# Why It Matters

该文支持 wiki 中 normalization/residuals 作为 serving-relevant architecture 的定位：它们影响训练稳定性、kernel fusion、block 边界和现代 decoder-only 结构。

# Connections

- Concept: [Transformer Normalization and Residuals](../concepts/transformer-normalization-and-residuals.md)
- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

# Open Questions

- 不同 norm 方案的最佳选择依赖模型深度、优化器、初始化和训练 recipe。
