# LLM Deployment and Capacity Planning

LLM deployment and capacity planning sits between model architecture and production operations. The current material emphasizes that reliable serving depends on correct GPU memory estimation, explicit performance targets, batching policy, and fast operational responses when resource pressure shows up in latency or error rates.

## Core Ideas

- Deployment variants should separate public production models from test-only configurations.
- Memory planning is not just parameter count; it includes runtime reservation, hardware reservation, and KV cache.
- User experience depends on separating TTFT, TPOT, overall latency, and throughput instead of collapsing them into one metric.
- Decode speed is often constrained by memory bandwidth, so hardware bandwidth and serving-stack efficiency matter as much as raw compute.
- Continuous batching is usually the right default for shared online serving, while static batching can still win for offline workloads.
- MoE deployments require explicit reasoning about what tensor parallelism splits and what expert parallelism splits.
- More GPUs and higher tensor parallelism usually improve fit and latency only sub-linearly because communication overhead and utilization losses rise.
- Quantization can reduce bandwidth and memory pressure, but it must be validated against model-quality regressions.
- Capacity incidents are often handled first through scaling or throttling rather than deep architectural changes.

## Related Concepts

- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- [Model Bandwidth Utilization](../concepts/model-bandwidth-utilization.md)
- [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
