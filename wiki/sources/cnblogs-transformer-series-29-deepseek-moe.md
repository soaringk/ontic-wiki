---
kind: source
title: "探秘Transformer系列之（29）--- DeepSeek MoE"
slug: cnblogs-transformer-series-29-deepseek-moe
source_ids:
  - raw-cnblogs-transformer-series-29-transformer-29-deepseek-moe
status: active
raw_path: raw/cnblogs-transformer-series/29-探秘Transformer系列之（29）--- DeepSeek MoE.md
source_type: markdown
parser: direct
published: 2025-04-20
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文介绍 DeepSeek MoE 的难点、DeepSeek V1/V2/V3 中的专家设计和其它探索，重点关注细粒度专家、共享专家、routing、负载均衡和通信效率。

# Key Claims

- DeepSeek MoE 通过细粒度 expert 和 shared expert 组合，试图在专家专业化、通用能力和路由稳定性之间折中。
- Routing 难点包括 token 分布不均、专家负载不均、训练不稳定和跨设备通信。
- Expert parallelism 对 serving 系统提出新的 token dispatch、all-to-all 通信和容量规划要求。
- MoE 增大参数容量时，每 token 激活参数受限，但 KV cache 与 attention 路径仍然存在。

# Why It Matters

该文把通用 MoE 概念落到 DeepSeek 架构演进上，补充 Mixture of Experts 和 parallelism 页面。

# Connections

- Concept: [Mixture of Experts](../concepts/mixture-of-experts.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- Concept: [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)

# Open Questions

- DeepSeek 具体实现细节应以官方论文/代码为准；本文适合作为中文学习解读。
