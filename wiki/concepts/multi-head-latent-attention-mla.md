# Multi-head Latent Attention (MLA)

MLA is an attention variant introduced by DeepSeek V2/V3 that compresses the per-token KV representation by projecting key and value into a shared low-dimensional latent space. Instead of caching full K and V tensors, it stores compressed latent state plus the required RoPE key component.

## Why It Matters

- The undated [KV-cache architecture survey](../sources/kv-cache-architecture-survey.md) reports a reduction from 14,336 to 576 cached dimensions at DeepSeek V3 scale, approximately 96%.
- The local sources do not establish a general no-degradation result; quality and serving benefit remain model- and implementation-dependent.
- MLA is orthogonal to GQA/MQA (which reduce KV head count) and can be combined with cross-layer attention or quantization for further compression.
- A naive implementation can reconstruct full per-head K/V on the fly, while optimized inference can absorb projection weights and avoid materializing those full tensors. Both paths trade additional projection structure for much smaller stored state.
- RoPE-related Q/K dimensions need separate handling from the compressible latent path, so implementation details matter for both correctness and actual serving benefit ([DeepSeek MLA tutorial](../sources/cnblogs-transformer-series-28-deepseek-mla.md)).

## Related Pages

- [Attention Mechanism](attention-mechanism.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](../sources/kv-cache-architecture-survey.md)
- [探秘Transformer系列之（28）--- DeepSeek MLA](../sources/cnblogs-transformer-series-28-deepseek-mla.md)
