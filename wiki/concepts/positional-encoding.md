# Positional Encoding

Positional encoding injects order information into Transformer computation so attention can distinguish sequences with the same tokens in different orders.

## Why It Matters

- Plain self-attention is permutation-equivariant: without position signals it cannot tell `猫追狗` from `狗追猫` using token order alone.
- Absolute position encodings add or learn a vector per position at the input layer, but tend to extrapolate poorly beyond training length.
- RoPE rotates Q and K by position-dependent angles so their dot product depends on relative position; V is left unrotated because it carries content rather than matching position.
- ALiBi adds a distance-dependent linear bias directly to attention scores, making extrapolation simple but less expressive than RoPE.
- Long-context RoPE extensions such as position interpolation, NTK-aware scaling, YaRN, and dynamic NTK adjust how frequencies scale beyond the training window.
- Position encoding choices affect kernel fusion, trigonometric cache layout, long-context quality, and KV Cache memory pressure.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [Attention Mechanism](attention-mechanism.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Tokenization and Embeddings](tokenization-and-embeddings.md)

## Sources

- [3.5 Transformer位置编码深入理解](../sources/transformer-positional-encoding-deep-dive.md)
- [3.9 Tokenization与词嵌入](../sources/tokenization-and-word-embedding.md)
- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
