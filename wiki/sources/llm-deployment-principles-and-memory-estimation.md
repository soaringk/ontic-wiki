---
kind: source
title: LLM Deployment Principles and Memory Estimation Cheat Sheet
slug: llm-deployment-principles-and-memory-estimation
source_ids:
  - raw-llm-model-calculation-cheat-sheet
status: active
raw_path: raw/llm_model_calculation_cheat_sheet.md
source_type: markdown
created: 2026-04-11
updated: 2026-04-11
---

# Summary

This source is an operational cheat sheet for large-model deployment. It combines naming and redundancy conventions with formulas for estimating GPU memory usage, especially model weights and KV cache, and closes with basic incident-recovery guidance based on capacity pressure and request failures.

# Key Claims

- Deployment policy should distinguish public models from test variants and keep production redundancy across clusters and replicas.
- GPU memory planning can be broken into model weights, runtime reserve, hardware reserve, and KV cache.
- For MoE models, tensor parallelism and expert parallelism split different parts of the parameter set, so memory formulas must treat dense layers, shared experts, and routed experts separately.
- KV cache sizing can be derived per token from layer count, KV heads, head dimension, precision, and tensor parallelism.
- Operational recovery for online serving is mostly a capacity problem: scale out or throttle when resource pressure, latency, or rate-limit errors rise.

# Why It Matters

The source bridges architecture details and on-call operations. It provides a compact model for estimating whether a deployment plan fits into GPU memory and what the first recovery actions should be when serving quality degrades.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

# Open Questions

- The formulas are practical but framework-specific in places, especially around embedding partitioning and runtime cache allocation.
- The recovery section is intentionally high level and does not specify alert thresholds, autoscaling triggers, or rollout policy.
