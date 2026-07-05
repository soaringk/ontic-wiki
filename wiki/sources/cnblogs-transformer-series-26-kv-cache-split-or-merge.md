---
kind: source
title: "探秘Transformer系列之（26）--- KV Cache优化---分离or合并"
slug: cnblogs-transformer-series-26-kv-cache-split-or-merge
source_ids:
  - raw-cnblogs-transformer-series-26-transformer-26-kv-cache-or
status: active
raw_path: raw/cnblogs-transformer-series/26-探秘Transformer系列之（26）--- KV Cache优化---分离or合并.md
source_type: markdown
parser: direct
published: 2025-04-12
created: 2026-07-04
updated: 2026-07-04
---

# Summary

本文比较 KV Cache 优化中的“融合派”和“分离方式”：静态批处理、prefill/decode 混合调度、chunked prefill、disaggregation，以及不同服务形态下把 prefill 与 decode 合并或分离的取舍。

# Key Claims

- Prefill 和 decode 在计算形态、batch 需求和资源瓶颈上不同；是否分离取决于 workload、SLO 和系统复杂度。
- 融合/共置方案通过 chunked prefill、continuous batching 等调度减少资源碎片和系统复杂度。
- 分离方案把 prefill 和 decode 放到不同实例或硬件池，减少互相干扰，但引入 KV transfer 和调度开销。
- 静态批处理适合离线吞吐，在线自回归服务更需要 iteration-level/continuous batching。

# Why It Matters

该文把 KV Cache 优化与 serving architecture 联系起来，补强 Disaggregated LLM Inference、Prefill-Decode Disaggregation 和 Chunked Prefill Scheduling 的共同边界。

# Connections

- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- Concept: [Chunked Prefill Scheduling](../concepts/chunked-prefill-scheduling.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)

# Open Questions

- 没有单一最优架构；共置和分离需要按 TTFT、TPOT、throughput、KV transfer 成本和运维复杂度权衡。
