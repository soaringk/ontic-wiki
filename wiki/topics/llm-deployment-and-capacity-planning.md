# LLM Deployment and Capacity Planning

LLM deployment and capacity planning sits between model architecture and production operations. The current material emphasizes that reliable serving depends on naming and redundancy discipline, correct GPU memory estimation, and fast operational responses when resource pressure shows up in latency or error rates.

## Core Ideas

- Deployment variants should separate public production models from test-only configurations.
- Memory planning is not just parameter count; it includes runtime reservation, hardware reservation, and KV cache.
- MoE deployments require explicit reasoning about what tensor parallelism splits and what expert parallelism splits.
- Capacity incidents are often handled first through scaling or throttling rather than deep architectural changes.

## Related Concepts

- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
