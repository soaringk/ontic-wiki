# LLM Deployment and Capacity Planning

LLM deployment and capacity planning sits between model architecture and production operations. The current material emphasizes that reliable serving depends on correct GPU memory estimation, explicit performance targets, batching policy, and fast operational responses when resource pressure shows up in latency or error rates.

## Core Ideas

- Deployment variants should separate public production models from test-only configurations.
- Memory planning is not just parameter count; it includes runtime reservation, hardware reservation, and KV cache.
- User experience depends on separating TTFT, TPOT, overall latency, and throughput instead of collapsing them into one metric.
- Decode speed is often constrained by memory bandwidth, so hardware bandwidth and serving-stack efficiency matter as much as raw compute.
- Continuous batching is usually the right default for shared online serving, while static batching can still win for offline workloads.
- Request-level scheduling is a poor fit for autoregressive generation; iteration-level control is the more durable systems model.
- Prefill and decode often want different batch sizes, parallelism strategies, and sometimes different hardware entirely.
- Prefix reuse, cache placement, and KV-state transfer are now first-class deployment concerns rather than narrow engine details.
- MoE deployments require explicit reasoning about what tensor parallelism splits and what expert parallelism splits.
- More GPUs and higher tensor parallelism usually improve fit and latency only sub-linearly because communication overhead and utilization losses rise.
- Quantization can reduce bandwidth and memory pressure, but it must be validated against model-quality regressions.
- Integer-only and quantization-aware approaches matter because real deployment wins come from arithmetic that hardware can execute efficiently, not only smaller checkpoint files.
- Capacity incidents are often handled first through scaling or throttling rather than deep architectural changes.

## Related Concepts

- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- [Model Bandwidth Utilization](../concepts/model-bandwidth-utilization.md)
- [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- [PagedAttention](../concepts/pagedattention.md)
- [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- [Integer-Only Quantization](../concepts/integer-only-quantization.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](../sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md)
- [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](../sources/splitwise-efficient-generative-llm-inference-using-phase-splitting.md)
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](../sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md)
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](../sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md)
- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](../sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md)
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](../sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md)
- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](../sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md)
- [How to Generate Tokens Faster: A vLLM Performance Model](../sources/vllm-performance-model.md)
