---
kind: source
title: "探秘Transformer系列之（34）--- 量化基础"
slug: cnblogs-transformer-series-34-quantization-basics
source_ids:
  - raw-cnblogs-transformer-series-34-transformer-34
status: active
raw_path: raw/cnblogs-transformer-series/34-探秘Transformer系列之（34）--- 量化基础.md
source_type: markdown
parser: direct
published: 2025-05-24
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍量化背景、浮点/定点表示、scale/zero-point、对称/非对称量化、per-tensor/per-channel、校准、PTQ/QAT 和量化误差。它为大模型量化方案提供基础概念。

# Key Claims

- 量化用低位整数或低精度格式近似高精度权重/激活，以降低内存、带宽和计算成本。
- Scale 与 zero-point 定义实数值到离散整数值的映射；对称/非对称方案在范围利用和硬件友好性上不同。
- Per-channel 量化通常比 per-tensor 更能适应不同通道分布，但元数据和实现复杂度更高。
- PTQ 成本低但易受分布和 outlier 影响；QAT 通常质量更稳但训练成本高。

# Why It Matters

该文扩展 Integer-Only Quantization 页面的基础，为后续 LLM.int8、GPTQ、AWQ、SmoothQuant 等方案建立共同语言。

# Connections

- Concept: [Integer-Only Quantization](../concepts/integer-only-quantization.md)
- Concept: [LLM Quantization](../concepts/llm-quantization.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- 量化收益只有在硬件和 kernel 能高效执行低精度路径时才会完全兑现。
