# Positional Encoding

Positional encoding injects order information into Transformer computation so attention can distinguish sequences with the same tokens in different orders.

## Why It Matters

- Plain self-attention is permutation-equivariant: without position signals it cannot tell `猫追狗` from `狗追猫` using token order alone.
- Absolute position encodings add or learn a vector per position at the input layer, but tend to extrapolate poorly beyond training length.
- RoPE rotates Q and K by position-dependent angles so their dot product depends on relative position; V is left unrotated because it carries content rather than matching position.
- ALiBi adds a distance-dependent linear bias directly to attention scores, making extrapolation simple but less expressive than RoPE.
- Long-context RoPE extensions such as position interpolation, NTK-aware scaling, YaRN, and dynamic NTK adjust how frequencies scale beyond the training window.
- Position encoding choices affect kernel fusion, trigonometric cache layout, long-context quality, and KV Cache memory pressure.
- Long-context extrapolation must be evaluated separately from maximum configured context length because position scaling can preserve syntax while still losing retrieval or reasoning quality on long documents.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [Attention Mechanism](attention-mechanism.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Tokenization and Embeddings](tokenization-and-embeddings.md)
- [Long Context Extrapolation](long-context-extrapolation.md)

## Sources

- [3.5 Transformer位置编码深入理解](../sources/transformer-positional-encoding-deep-dive.md)
- [3.9 Tokenization与词嵌入](../sources/tokenization-and-word-embedding.md)
- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
- [探秘Transformer系列之（8）--- 位置编码](../sources/cnblogs-transformer-series-08-positional-encoding.md)
- [探秘Transformer系列之（9）--- 位置编码分类](../sources/cnblogs-transformer-series-09-positional-encoding-taxonomy.md)
- [探秘Transformer系列之（17）--- RoPE](../sources/cnblogs-transformer-series-17-rope.md)
- [探秘Transformer系列之（23）--- 长度外推](../sources/cnblogs-transformer-series-23-length-extrapolation.md)
