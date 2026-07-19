# Multi-head Latent Attention (MLA)

MLA is an attention variant introduced by DeepSeek V2/V3 that compresses the per-token KV representation by projecting key and value into a shared low-dimensional latent space. Instead of caching full K and V tensors, only the low-rank latent vector `c` is stored and reconstructed during attention computation.

## Why It Matters

- The undated [KV-cache architecture survey](../sources/kv-cache-architecture-survey.md) reports a reduction from 14,336 to 576 cached dimensions at DeepSeek V3 scale, approximately 96%.
- The local sources do not establish a general no-degradation result; quality and serving benefit remain model- and implementation-dependent.
- MLA is orthogonal to GQA/MQA (which reduce KV head count) and can be combined with cross-layer attention or quantization for further compression.
- The cached latent is reconstructed to full K/V on-the-fly during attention computation, trading extra projection work for much smaller stored state.
- RoPE-related Q/K dimensions need separate handling from the compressible latent path, so implementation details matter for both correctness and actual serving benefit ([DeepSeek MLA tutorial](../sources/cnblogs-transformer-series-28-deepseek-mla.md)).

## Related Pages

- [Attention Mechanism](attention-mechanism.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](../sources/kv-cache-architecture-survey.md)
- [探秘Transformer系列之（28）--- DeepSeek MLA](../sources/cnblogs-transformer-series-28-deepseek-mla.md)
