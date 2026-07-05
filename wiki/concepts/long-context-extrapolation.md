# Long Context Extrapolation

Long context extrapolation is the problem of making a Transformer remain useful at sequence lengths beyond the length distribution it was trained on.

## Why It Matters

- Extending context length is not just a memory problem; the model also sees position signals and attention-score distributions outside its training regime.
- RoPE-based models often need position interpolation, frequency scaling, or segmented scaling to reduce mismatch between trained and served context lengths.
- Longer context increases KV-cache memory and decode bandwidth even when the position encoding extrapolates acceptably.
- Sparse attention, context caching, retrieval, and KV compression can reduce long-context serving cost, but they may change what information the model can access.
- Effective long-context quality must be measured on long-document tasks, not inferred from maximum configured context window.

## Related Pages

- [Positional Encoding](positional-encoding.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Context Caching in LLM Serving](context-caching-in-llm-serving.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [探秘Transformer系列之（23）--- 长度外推](../sources/cnblogs-transformer-series-23-length-extrapolation.md)
- [探秘Transformer系列之（25）--- KV Cache优化之处理长文本序列](../sources/cnblogs-transformer-series-25-kv-cache-long-context.md)
- [3.5 Transformer位置编码深入理解](../sources/transformer-positional-encoding-deep-dive.md)
