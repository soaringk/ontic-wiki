---
kind: source
title: "探秘Transformer系列之（16）--- 资源占用"
slug: cnblogs-transformer-series-16-resource-usage
source_ids:
  - raw-cnblogs-transformer-series-16-transformer-16
status: active
raw_path: raw/cnblogs-transformer-series/16-探秘Transformer系列之（16）--- 资源占用.md
source_type: markdown
parser: direct
published: 2025-03-21
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文估算 Transformer 参数量、显存占用、计算量和优化方向，覆盖 embedding/LM head、attention、FFN、activation、optimizer state、训练/推理显存差异和 FLOPs 组成。

# Key Claims

- Transformer 资源占用应拆成参数、激活、梯度、优化器状态、KV cache 和临时 workspace，而不是只看 checkpoint 大小。
- FFN 通常贡献大量参数和 GEMM 计算，attention 的序列长度项和 KV cache 则在长上下文/推理场景中主导成本。
- 训练显存与推理显存结构不同；训练需要保存激活、梯度和优化器状态，推理更关注权重、KV cache 和 batch/context 长度。
- 优化方向包括并行、混合精度/量化、activation checkpointing、attention kernel 优化和 KV cache 优化。

# Why It Matters

该文直接服务于 LLM Deployment and Capacity Planning：它把模型结构变成可估算的内存和计算预算。

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

# Open Questions

- 公式是 planning 工具；真实占用需要用具体框架、dtype、parallelism 和 kernel 实现验证。
