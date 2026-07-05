---
kind: source
title: "探秘Transformer系列之（22）--- LoRA"
slug: cnblogs-transformer-series-22-lora
source_ids:
  - raw-cnblogs-transformer-series-22-transformer-22-lora
status: active
raw_path: raw/cnblogs-transformer-series/22-探秘Transformer系列之（22）--- LoRA.md
source_type: markdown
parser: direct
published: 2025-04-03
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 LoRA 的背景知识、低秩适配原理、复杂度与资源占用、支撑机理、实现和改进。核心思想是在冻结原模型权重的基础上，为目标线性层添加低秩增量矩阵进行参数高效微调。

# Key Claims

- LoRA 假设任务适配所需权重更新具有低内在秩，因此可用 `B A` 形式的低秩矩阵近似全量权重增量。
- 训练时冻结 base model，只训练 LoRA adapter，显著减少可训练参数、优化器状态和显存需求。
- 推理时 LoRA 权重可以与原权重合并，也可以作为可切换 adapter 动态加载。
- LoRA rank、alpha、dropout、插入层选择和目标模块会共同影响质量、资源占用和过拟合风险。

# Why It Matters

该文为 wiki 新增参数高效微调视角，连接模型部署中的 adapter 管理、多租户定制和低成本领域适配。

# Connections

- Concept: [Low-Rank Adaptation (LoRA)](../concepts/low-rank-adaptation-lora.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)

# Open Questions

- LoRA 的最佳目标层和 rank 需要任务验证；低秩假设不是所有适配场景都同样成立。
