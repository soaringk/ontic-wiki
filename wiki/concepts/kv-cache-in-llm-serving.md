# KV Cache in LLM Serving

KV cache stores attention keys and values for prior tokens so later decoding steps do not recompute them from scratch.

## Why It Matters

- KV cache is often the largest variable part of inference-time GPU memory.
- Maximum supported context length depends on how much cache memory is available and how much memory each token consumes.
- Cache size depends on layer count, KV head count, head dimension, cache precision, and tensor parallelism.

## Durable Formula Shape

The source frames per-token cache roughly as proportional to:

`2 * num_hidden_layers * num_key_value_heads * head_dim * kvcache_dtype_byte / TP`

The factor of 2 comes from caching both K and V tensors.

## Operational Use

- Read engine/runtime logs for the actual cache allocation when available.
- Treat the formula as a planning tool, then confirm with the serving framework's real allocation behavior.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [Parallelism in LLM Serving](parallelism-in-llm-serving.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
