---
kind: source
title: "探秘Transformer系列之（36）--- 大模型量化方案"
slug: cnblogs-transformer-series-36-llm-quantization-methods
source_ids:
  - raw-cnblogs-transformer-series-36-transformer-36
status: active
raw_path: raw/cnblogs-transformer-series/36-探秘Transformer系列之（36）--- 大模型量化方案.md
source_type: markdown
parser: direct
published: 2025-06-08
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文按 8-bit、4-bit 和更低位量化方案梳理 LLM 量化方法，覆盖 LLM.int8、SmoothQuant、GPTQ、AWQ、QLoRA、KV cache/activation 量化等方向。

# Key Claims

- 8-bit 方案通常更容易保持质量，重点在 outlier 处理和激活平滑。
- 4-bit 权重量化显著降低模型内存，但需要分组、校准、误差补偿或激活感知策略来保持质量。
- QLoRA 把 4-bit base model 与 LoRA adapter 结合，降低微调显存门槛。
- 更低位量化和 KV cache 量化可以继续降成本，但质量、kernel 支持和硬件路径风险更高。

# Why It Matters

该文把量化基础落到部署可选方案上，连接 LoRA、capacity planning、KV cache 和 integer-only quantization。

# Connections

- Concept: [LLM Quantization](../concepts/llm-quantization.md)
- Concept: [Low-Rank Adaptation (LoRA)](../concepts/low-rank-adaptation-lora.md)
- Concept: [Integer-Only Quantization](../concepts/integer-only-quantization.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- Scheme names are not enough for deployment choice; compare model quality, latency, memory, supported kernels, and operational tooling.
