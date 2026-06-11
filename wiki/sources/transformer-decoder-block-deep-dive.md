---
kind: source
title: "3.7 Transformer Decoder Block完整解析"
slug: transformer-decoder-block-deep-dive
source_ids:
  - raw-aiinfraguide-3-7-transformer-decoder-block
status: active
raw_path: raw/AIInfraGuide/3.7 Transformer Decoder Block完整解析.md
source_type: markdown
parser: direct
published: 2026-04-21
created: 2026-06-11
updated: 2026-06-11
---

# Summary

这篇文章把 Decoder-only Transformer Block 拆解为 RMSNorm、Masked Multi-Head Attention、RoPE、SwiGLU FFN 和残差连接，并用 LLaMA 类配置推导参数量、FLOPs 和显存规划。

# Key Claims

- Decoder-only 架构用统一的 next-token prediction 训练目标和重复堆叠的同构 Block，降低了数据构造、扩展和推理系统复杂度。
- Causal mask 通过屏蔽未来 token 维持自回归约束；高性能实现通常不显式 materialize 完整 `N x N` 掩码。
- 当前主流 Decoder Block 数据流通常是 `RMSNorm -> masked attention -> residual -> RMSNorm -> SwiGLU FFN -> residual`。
- 参数量估算应拆分 embedding、每层 attention、FFN、norm 和 LM head；FFN 通常占单个 Block 约三分之二参数。
- 推理显存要分开计算权重和 KV Cache；训练显存还要加入梯度、优化器状态和 activation。
- GQA、RoPE、RMSNorm、SwiGLU、MoE、MLA 和大词表都是架构选择，同时也是系统容量规划变量。

# Why It Matters

这篇文章提供了从模型结构到可手算容量规划的完整路径，适合作为 Transformer 架构、参数量估算、KV Cache 公式和 GPU fit 判断的共同入口。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- Concept: [Transformer Normalization and Residuals](../concepts/transformer-normalization-and-residuals.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

# Source Notes

- Canonical raw capture: `raw/AIInfraGuide/3.7 Transformer Decoder Block完整解析.md`.
- Local raw corrects the Attention FLOPs coefficient in the upstream Markdown formula from `2` to `4`.

# Open Questions

- 参数量和显存公式适合规划，但实际部署仍需检查具体框架的权重 tying、KV dtype、buffer 和并行切分行为。
