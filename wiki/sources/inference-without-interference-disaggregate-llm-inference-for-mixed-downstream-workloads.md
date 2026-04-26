---
kind: source
title: Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads
slug: inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads
source_ids:
  - raw-prefill-decode-separation-2401-11181v1
status: active
raw_path: raw/prefill-decode-separation/2401.11181v1.pdf
source_type: pdf
published: unknown
created: 2026-04-25
updated: 2026-04-27
---

# Summary

This paper studies interference explicitly across mixed workloads and argues that different request shapes should influence both prefill and decode scheduling. TetriInfer combines disaggregation with fixed-size chunked prefill and decode-side length-aware scheduling to reduce cross-workload contention.

# Key Claims

- Interference is not only between prefill and decode; different prefill sizes and different decode lengths can also hurt each other.
- Hardware should avoid pushing prefill past the accelerator-saturation threshold, so prompts are chunked into fixed-size compute units.
- Decode scheduling benefits from predicted generation-length buckets rather than naive FIFO treatment.
- Mixed downstream workloads need scheduling that is aware of resource usage, not just arrival order.
- Disaggregated instances can change roles and scale independently as workload balance shifts.

# Why It Matters

This source sharpens the notion of interference. It shows that disaggregation alone is not enough; once phases are separated, the scheduler still needs workload-shape awareness to avoid recreating hotspots inside each pool.

# Connections

- Topic: [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- Concept: [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)

# Open Questions

- The length-prediction component is useful but introduces its own cost and modeling risk, and the paper leaves the prediction-quality ceiling mostly open.
- Some gains depend on specific workload mixes, and the authors note weaker benefits on heavy-prefill plus heavy-decode cases.
