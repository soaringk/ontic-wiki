---
kind: source
title: "3.8 从Transformer到LLM自回归生成深入理解"
slug: transformer-to-llm-autoregressive-generation
source_ids:
  - raw-aiinfraguide-3-8-transformer-llm
status: active
raw_path: raw/AIInfraGuide/3.8 从Transformer到LLM自回归生成深入理解.md
source_type: markdown
parser: direct
published: 2026-04-21
created: 2026-06-11
updated: 2026-06-11
---

# Summary

这篇文章从条件概率解释语言模型与自回归生成，覆盖采样策略、Prefill/Decode 两阶段、KV Cache、PagedAttention、Prefix Cache、GQA/MQA、Sliding Window、Speculative Decoding 和推理性能指标。

# Key Claims

- 自回归语言模型把联合概率分解为逐 token 条件概率，每一步基于已有上下文预测并采样下一个 token。
- Greedy、Temperature、Top-K 和 Top-P 调整的是从 logits 到下一个 token 的选择策略，直接影响确定性、多样性和退化风险。
- Prefill 一次处理完整 prompt 并建立初始 KV Cache，通常 compute-bound，决定 TTFT。
- Decode 每步只处理一个新 token，但要读取权重和已有 KV Cache，通常 memory-bound，决定 TPOT。
- KV Cache 避免重复计算历史 token 的 K/V，把自回归生成中的大量重复 QKV 投影从每步全前缀重算降为只追加新 token。
- PagedAttention 用固定大小块和 block table 管理 KV Cache，减少连续预分配带来的浪费和碎片化。
- 系统级优化包括 Continuous Batching、Prefix Cache、KV 量化、GQA/MQA、Sliding Window、Prefill/Decode 解耦和 Speculative Decoding。

# Why It Matters

这篇文章把 Transformer 机制转化为推理系统语言：TTFT、TPOT、throughput、KV Cache、batching 和调度策略都来自自回归生成的计算形态。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [PagedAttention](../concepts/pagedattention.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)

# Source Notes

- Canonical raw capture: `raw/AIInfraGuide/3.8 从Transformer到LLM自回归生成深入理解.md`.

# Open Questions

- Speculative Decoding and KV eviction require model- and workload-specific validation before being treated as quality-neutral production defaults.
