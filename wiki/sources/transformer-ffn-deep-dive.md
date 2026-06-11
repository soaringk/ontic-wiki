---
kind: source
title: "3.4 Transformer前馈网络FFN深入理解"
slug: transformer-ffn-deep-dive
source_ids:
  - raw-aiinfraguide-3-4-transformer-ffn
status: active
raw_path: raw/AIInfraGuide/3.4 Transformer前馈网络FFN深入理解.md
source_type: markdown
parser: direct
published: 2026-04-20
created: 2026-06-11
updated: 2026-06-11
---

# Summary

这篇 AI Infra Guide 文章把 Transformer FFN 作为 Decoder Block 中参数量最大的计算模块来解释，覆盖标准 FFN、GELU/Swish/SwiGLU、参数量估算、张量并行、MoE 专家化，以及 FFN kernel 融合。

# Key Claims

- Self-Attention 负责 token 间信息交互，FFN 对每个 token 独立做非线性加工，是 Transformer 表达能力和参数容量的主要来源。
- 标准 FFN 使用 `d_model -> d_ff -> d_model` 的展开-压缩结构；常见 `d_ff = 4 * d_model` 让非线性变换在更高维空间中发生。
- SwiGLU 用 `W_gate` 和 `W_up` 两条路径做门控筛选，通常把中间维度设为约 `8/3 * d_model`，以在三矩阵结构下维持接近标准 FFN 的总参数量。
- 单个 Decoder Block 中 FFN 参数量通常约为 Attention 的两倍，因此 FFN 是量化、并行切分、MoE 化和 kernel 融合的重要目标。
- Megatron-LM 风格的 FFN 张量并行通常对 `W_up/W_gate` 做列切分，对 `W_down` 做行切分，使中间激活可本地计算，最终只需一次 AllReduce。
- MoE 本质上把 FFN 拆成多个专家，并用路由器只激活少数专家；它扩大总参数容量，但引入专家并行、All-to-All 和负载均衡问题。

# Why It Matters

这篇文章强化了 Transformer 架构与系统优化之间的连接：FFN 不只是数学子层，也是推理延迟、参数显存、张量并行、MoE 通信和 kernel fusion 的核心对象。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

# Source Notes

- Canonical raw capture: `raw/AIInfraGuide/3.4 Transformer前馈网络FFN深入理解.md`.

# Open Questions

- 具体 kernel fusion 收益依赖硬件、batch shape、prefill/decode 阶段和框架实现，应与运行时 benchmark 一起使用。
