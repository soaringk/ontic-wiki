---
kind: source
title: "3.6 LayerNorm与残差连接深入理解"
slug: layernorm-and-residual-connections-deep-dive
source_ids:
  - raw-aiinfraguide-3-6-layernorm
status: active
raw_path: raw/AIInfraGuide/3.6 LayerNorm与残差连接深入理解.md
source_type: markdown
parser: direct
published: 2026-04-21
created: 2026-06-11
updated: 2026-06-11
---

# Summary

这篇文章解释深层 Transformer 为什么需要残差连接和归一化，比较 BatchNorm、LayerNorm、RMSNorm、Pre-Norm、Post-Norm 和 DeepNorm，并从 CUDA kernel 角度讨论归一化与残差加法融合。

# Key Claims

- 深层网络训练的根本困难来自梯度消失、梯度爆炸和退化问题；残差连接通过恒等路径让梯度可以跨层直达。
- LayerNorm 沿特征维度对每个 token 独立归一化，因此不依赖 batch size、序列长度或训练/推理统计量，适合 Transformer。
- RMSNorm 去掉均值中心化，只保留 RMS 缩放和缩放参数，通常以更低内存带宽开销得到接近 LayerNorm 的稳定性。
- Pre-Norm 将归一化放在子层前，使残差路径保持干净；Post-Norm 的残差输出还要过 LayerNorm，更容易在深层训练中出现不稳定。
- Residual Add + LayerNorm/RMSNorm 是常见融合 kernel 边界，因为分开执行会把中间结果写回再读出 HBM。
- 半精度训练中归一化 reduction 通常需要 FP32 累加，避免 FP16 求和、平方和方差计算的数值风险。

# Why It Matters

这篇文章补足了 Transformer 可训练性与工程实现之间的桥梁：模型能否训练、推理 kernel 如何融合、BF16/FP16 如何安全处理，都与残差和归一化位置直接相关。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Transformer Normalization and Residuals](../concepts/transformer-normalization-and-residuals.md)

# Source Notes

- Canonical raw capture: `raw/AIInfraGuide/3.6 LayerNorm与残差连接深入理解.md`.

# Open Questions

- Pre-Norm 是大模型默认工程选择，但特定训练配方下 Post-Norm/DeepNorm 仍可能有价值，需要结合规模和稳定性目标判断。
