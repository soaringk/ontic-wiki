# Parallel Decoding Variants

Parallel decoding variants try to reduce the serial bottleneck of autoregressive generation by proposing or predicting multiple future tokens before committing them.

## Why It Matters

- Autoregressive generation is inherently sequential at the commitment boundary, but candidate generation and verification can be parallelized.
- Speculative decoding uses draft candidates plus target-model verification, often preserving the target distribution when rejection sampling is exact.
- Medusa attaches multiple future-token heads to the base model and verifies tree-structured candidate continuations.
- Lookahead decoding generates and verifies candidates at inference time without necessarily training a separate draft model.
- Multi-token prediction trains models or auxiliary modules to predict multiple future offsets, potentially improving candidate quality for decoding acceleration.
- Throughput gains depend on candidate acceptance rate, verification cost, batch interference, KV-cache handling, and whether the serving engine can exploit the extra parallel work.

## Related Pages

- [Speculative Decoding](speculative-decoding.md)
- [Autoregressive Generation](autoregressive-generation.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

## Sources

- [探秘Transformer系列之（30）--- 投机解码](../sources/cnblogs-transformer-series-30-speculative-decoding.md)
- [探秘Transformer系列之（31）--- Medusa](../sources/cnblogs-transformer-series-31-medusa.md)
- [探秘Transformer系列之（32）--- Lookahead Decoding](../sources/cnblogs-transformer-series-32-lookahead-decoding.md)
- [探秘Transformer系列之（33）--- DeepSeek MTP](../sources/cnblogs-transformer-series-33-deepseek-mtp.md)
- [Accelerating Large Language Model Decoding with Speculative Sampling](../sources/accelerating-large-language-model-decoding-with-speculative-sampling.md)
