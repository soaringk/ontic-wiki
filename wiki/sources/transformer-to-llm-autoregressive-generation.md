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

这篇文章从条件概率解释语言模型与自回归生成，覆盖从 logits 到采样、Prefill/Decode 两阶段、KV Cache、PagedAttention、Prefix Cache、GQA/MQA、Sliding Window、Speculative Decoding、张量并行和推理性能指标。

# Key Claims

- 自回归语言模型把联合概率分解为逐 token 条件概率，每一步基于已有上下文预测并采样下一个 token。
- Greedy、Temperature、Top-K 和 Top-P 调整的是从 logits 到下一个 token 的选择策略，直接影响确定性、多样性和退化风险。
- Prefill 一次处理完整 prompt 并建立初始 KV Cache，通常 compute-bound，决定 TTFT。
- Decode 每步只处理一个新 token，但要读取权重和已有 KV Cache，通常 memory-bound，决定 TPOT。
- KV Cache 避免重复计算历史 token 的 K/V；无缓存自回归每步重跑完整前缀，Attention 总量为 $O(N^3 d)$，缓存后每步只有 1 个新 query 读历史 K/V，Attention 总量降为 $O(N^2 d)$。
- PagedAttention 用固定大小块和 block table 管理 KV Cache，减少连续预分配带来的浪费和碎片化。
- KV Cache 优化可以在管理层、复用层、数值层和架构层发生：PagedAttention 处理碎片化，Prefix/Radix Cache 复用共享前缀，KV 量化降低元素字节数，GQA/MQA/Sliding Window 减少需要保存或读取的 KV。
- 系统级优化包括 Continuous Batching、Prefill/Decode 解耦、Speculative Decoding 和推理张量并行；它们分别回应请求生命周期错位、两阶段资源需求差异、自回归串行瓶颈和单步延迟压力。
- 延迟、吞吐和成本要分开度量：TTFT、TPOT、E2E latency、tokens/s、requests/s、GPU utilization、$/1K tokens 会把不同瓶颈暴露出来。

# Why It Matters

这篇文章把 Transformer 机制转化为推理系统语言：TTFT、TPOT、throughput、KV Cache、batching 和调度策略都来自自回归生成的计算形态。

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Autoregressive Generation](../concepts/autoregressive-generation.md)
- Concept: [Token Sampling Strategies](../concepts/token-sampling-strategies.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [PagedAttention](../concepts/pagedattention.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- Concept: [Speculative Decoding](../concepts/speculative-decoding.md)

# Source Notes

- Canonical raw capture: `raw/AIInfraGuide/3.8 从Transformer到LLM自回归生成深入理解.md`.
- Raw frontmatter publishes the source as `2026-04-21` and tags it with `Transformer`, `自回归生成`, `KV Cache`, and `PagedAttention`.
- Section 6.2 has a local erratum: without KV Cache, the autoregressive no-cache path uses full-prefix $Q,K,V$ matrices at each step, so the Attention sum is $\sum_{n=1}^{N} n^2 d = O(N^3 d)$, not $O(N^2 d)$.

# Open Questions

- Speculative Decoding, KV Cache quantization, and KV eviction require model- and workload-specific validation before being treated as quality-neutral production defaults.
