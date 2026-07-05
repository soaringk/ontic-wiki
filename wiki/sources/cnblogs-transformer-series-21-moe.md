---
kind: source
title: "探秘Transformer系列之（21）--- MoE"
slug: cnblogs-transformer-series-21-moe
source_ids:
  - raw-cnblogs-transformer-series-21-transformer-21-moe
status: active
raw_path: raw/cnblogs-transformer-series/21-探秘Transformer系列之（21）--- MoE.md
source_type: markdown
parser: direct
published: 2025-03-31
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文系统介绍 Mixture of Experts 的前置知识、发展历史、模型结构、计算流程和并行计算。它把 MoE 描述为用 routing/gating 在多个专家 FFN 中选择少数专家激活，从而扩大参数容量而控制每 token 计算量。

# Key Claims

- MoE 通常替换或扩展 Transformer FFN 路径，用多个 expert 承载容量，并由 router 为每个 token 选择 top-k expert。
- 稀疏激活让总参数量增长快于实际每 token FLOPs，但带来负载均衡、通信和路由稳定性问题。
- Expert parallelism 与 tensor/data/pipeline parallelism 不同，需要按专家分布和 token dispatch/reduce 来规划通信。
- MoE serving 的难点包括专家负载不均、跨设备通信、batch 内 token 分布和 cache/activation 内存结构变化。

# Why It Matters

该文补充 wiki 对 FFN 演进和 LLM deployment parallelism 的覆盖，说明 MoE 是容量扩展方案，不只是模型结构名词。

# Connections

- Concept: [Mixture of Experts](../concepts/mixture-of-experts.md)
- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- MoE 的质量、成本和延迟收益高度依赖 routing、负载均衡损失、并行拓扑和服务负载。
