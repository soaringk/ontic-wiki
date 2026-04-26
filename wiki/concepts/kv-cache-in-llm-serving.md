# KV Cache in LLM Serving

KV cache stores attention keys and values for prior tokens so later decoding steps do not recompute them from scratch.

## Why It Matters

- KV cache is often the largest variable part of inference-time GPU memory.
- Maximum supported context length depends on how much cache memory is available and how much memory each token consumes.
- Cache size depends on layer count, KV head count, head dimension, cache precision, and tensor parallelism.
- Large batches and long generations can make cache growth the limiting factor for otherwise efficient shared serving.
- GQA and MQA reduce KV-cache footprint by sharing keys and values across more attention heads.
- Cache management policy matters as much as cache size: fragmentation, sharing, reuse, transfer, and swapping all change effective capacity.
- In disaggregated systems, KV cache becomes distributed state that may move across prefill, decode, DRAM, or lower storage tiers.

## Durable Formula Shape

The source frames per-token cache roughly as proportional to:

`2 * num_hidden_layers * num_key_value_heads * head_dim * kvcache_dtype_byte / TP`

The factor of 2 comes from caching both K and V tensors.

## Operational Use

- Read engine/runtime logs for the actual cache allocation when available.
- Treat the formula as a planning tool, then confirm with the serving framework's real allocation behavior.
- Evaluate cache quantization carefully because memory savings can be real but quality impact is model-dependent.
- Distinguish active per-request KV state from reusable historical prefix cache, because they create different routing and consistency questions.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [Model Bandwidth Utilization](model-bandwidth-utilization.md)
- [Parallelism in LLM Serving](parallelism-in-llm-serving.md)
- [PagedAttention](pagedattention.md)
- [Context Caching in LLM Serving](context-caching-in-llm-serving.md)
- [Prefill-Decode Disaggregation](prefill-decode-disaggregation.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](../sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md)
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](../sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md)
- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
