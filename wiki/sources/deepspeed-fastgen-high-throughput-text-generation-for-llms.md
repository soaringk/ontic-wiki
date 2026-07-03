---
kind: source
title: "DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference"
slug: deepspeed-fastgen-high-throughput-text-generation-for-llms
source_ids:
  - raw-2401-08671v1
status: active
raw_path: raw/2401.08671v1.pdf
source_type: pdf
parser: mineru
published: unknown
created: 2026-07-02
updated: 2026-07-02
---

# Summary

DeepSpeed-FastGen is a Microsoft DeepSpeed serving system built from DeepSpeed-MII and DeepSpeed-Inference. Its central scheduling idea, Dynamic SplitFuse, mixes prompt-processing tokens and generation tokens into consistent-size forward passes so long prompts do not stall streaming generation and short prompts can fill the GPU's high-throughput region.

# Key Claims

- Forward-pass latency is driven more by the total number of tokens in a pass than by the number of sequences in the batch.
- LLM inference has a throughput-saturation region: small token counts are memory-transfer limited, while larger token counts better saturate compute.
- Long prompts should be decomposed across multiple iterations instead of monopolizing one large prefill pass.
- Short prompts can be fused to fill a target token budget, keeping forward-pass sizes more uniform.
- Compared with vLLM in the reported benchmarks, DeepSpeed-FastGen claims up to 2.3x higher effective throughput, 2x lower average latency, and up to 3.7x lower token-level tail latency.

# Why It Matters

This source is useful because it treats batching as token-budget composition rather than only request admission. It reinforces the broader wiki pattern that prefill/decode interference can be mitigated either by physical disaggregation or by schedulers that bound per-iteration prompt work.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Concept: [Chunked Prefill Scheduling](../concepts/chunked-prefill-scheduling.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)

# Open Questions

- The paper presents an alpha release and roadmap, so some operational claims depend on later software maturity and model coverage.
- Dynamic SplitFuse is a colocated scheduling technique; it does not remove the separate questions of KV-cache placement, prefix reuse, and phase-specialized hardware that arise in disaggregated serving.
