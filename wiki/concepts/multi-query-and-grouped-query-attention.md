# Multi-Query and Grouped-Query Attention

Multi-Query Attention (MQA) and Grouped-Query Attention (GQA) retain multiple query heads while sharing fewer key/value heads. MQA shares one K/V pair across all query heads; GQA divides query heads into groups and shares one K/V pair within each group.

## Why It Matters

- Fewer K/V heads reduce KV-cache memory and decode-time memory bandwidth relative to standard multi-head attention.
- MQA maximizes sharing, while GQA offers an intermediate trade-off between MHA's separate K/V heads and MQA's single shared pair.
- Quality, checkpoint conversion, and kernel support are model- and implementation-dependent, so cache savings alone do not determine the best variant.
- MLA reduces stored KV state through latent compression rather than head sharing; the local material does not establish general composability between these mechanisms.

## Related Pages

- [Attention Mechanism](attention-mechanism.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Multi-head Latent Attention (MLA)](multi-head-latent-attention-mla.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [探秘Transformer系列之（27）--- MQA & GQA](../sources/cnblogs-transformer-series-27-mqa-and-gqa.md)
- [探秘Transformer系列之（12）--- 多头自注意力](../sources/cnblogs-transformer-series-12-multi-head-self-attention.md)
