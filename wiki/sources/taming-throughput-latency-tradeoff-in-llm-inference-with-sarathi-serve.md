---
kind: source
title: "Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve"
slug: taming-throughput-latency-tradeoff-in-llm-inference-with-sarathi-serve
source_ids:
  - raw-2403-02310v3
status: active
raw_path: raw/2403.02310v3.pdf
source_type: pdf
parser: mineru
published: unknown
created: 2026-07-02
updated: 2026-07-02
---

# Summary

Sarathi-Serve is an LLM inference scheduler that targets the throughput-latency trade-off in online serving. It uses chunked prefills plus stall-free batching to admit new requests without pausing ongoing decodes, while forming more uniform hybrid batches for tensor- and pipeline-parallel deployments.

# Key Claims

- Prefill-prioritizing schedulers such as vLLM improve throughput but can create generation stalls and high P99 time-between-tokens (TBT).
- Decode-prioritizing request-level schedulers protect TBT but waste throughput because the batch drains slowly as requests finish.
- Decode iterations are often memory-bound, leaving arithmetic slack that can be used for bounded amounts of prefill work.
- Chunked prefills split prompt processing into token-budgeted pieces so long prompts do not dominate a single iteration.
- Stall-free batching first includes ongoing decodes, then fills remaining token budget with prefill chunks; the token budget is tuned against the TBT SLO, hardware, and parallelism setup.
- The reported evaluation shows up to 2.6x higher serving capacity for Mistral-7B on one A100 and up to 5.6x for Falcon-180B across 8 A100 GPUs.

# Why It Matters

Sarathi-Serve gives a concrete scheduler-level alternative to full prefill/decode disaggregation. It shows that colocated serving can still reduce interference if prompt work is bounded per iteration and if batch construction is driven by token budget rather than request count alone.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Concept: [Chunked Prefill Scheduling](../concepts/chunked-prefill-scheduling.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- Concept: [Model Bandwidth Utilization](../concepts/model-bandwidth-utilization.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)

# Open Questions

- Token-budget selection is deployment-specific and depends on profiling, TBT SLOs, pipeline-parallel bubbles, and hardware tile effects.
- The authors leave a quantitative comparison with fully disaggregated systems to future work, especially where KV-cache transfer and prefill-replica memory underutilization change the cost model.
