---
kind: source
title: "探秘Transformer系列之（35）--- 大模型量化基础"
slug: cnblogs-transformer-series-35-llm-quantization-basics
source_ids:
  - raw-cnblogs-transformer-series-35-transformer-35
status: active
raw_path: raw/cnblogs-transformer-series/35-探秘Transformer系列之（35）--- 大模型量化基础.md
source_type: markdown
parser: direct
published: 2025-06-02
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文聚焦 LLM 量化中的 outlier、超异常值和 Transformer 量化难点。它解释为什么普通低位量化在大模型上容易因激活分布极端值、层间差异和 attention/FFN 结构而出现质量下降。

# Key Claims

- LLM 激活中常出现 outlier channel/token，使统一量化范围被少数极端值拉大，降低普通值分辨率。
- 超异常值和层间分布差异要求使用平滑、分组、混合精度或特殊 outlier 处理。
- Transformer 量化要分别考虑权重、激活、KV cache、attention score、FFN 和 LM head 的分布差异。
- 大模型量化不是单纯把 dtype 改小，而是误差分配、校准数据和硬件执行路径共同优化。

# Why It Matters

该文说明 LLM 量化的核心难点来自模型分布而非编码格式本身，补充容量规划中的“量化必须验证质量”原则。

# Connections

- Concept: [LLM Quantization](../concepts/llm-quantization.md)
- Concept: [Integer-Only Quantization](../concepts/integer-only-quantization.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Open Questions

- 不同模型家族和任务对 outlier 处理敏感度不同，需要实测 perplexity、任务指标和人工质量。
