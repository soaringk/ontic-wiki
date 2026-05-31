# Multi-head Latent Attention (MLA)

MLA is an attention variant introduced by DeepSeek V2/V3 that compresses the per-token KV representation by projecting key and value into a shared low-dimensional latent space. Instead of caching full K and V tensors, only the low-rank latent vector `c` is stored and reconstructed during attention computation.

## Why It Matters

- At DeepSeek V3 scale, MLA reduces per-layer KV storage from `2 × hidden_size` (MHA baseline) to `kv_lora_rank + qk_rope_head_dim = 512 + 64 = 576` dimensions — a ~96% reduction from a 14,336-dimension baseline.
- Model quality does not degrade; the joint compression acts as a regularizer.
- MLA is orthogonal to GQA/MQA (which reduce KV head count) and can be combined with cross-layer attention or quantization for further compression.
- The cached latent is reconstructed to full K/V on-the-fly during attention computation, trading extra projection work for much smaller stored state.

## Related Pages

- [Attention Mechanism](attention-mechanism.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](../sources/kv-cache-architecture-survey.md)
