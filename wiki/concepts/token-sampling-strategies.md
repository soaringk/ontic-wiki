# Token Sampling Strategies

Token sampling strategies choose the next token from a model's logits during autoregressive generation.

## Why It Matters

- Greedy decoding always chooses the highest-probability token, making output deterministic but more prone to repetition or bland continuations.
- Temperature rescales logits before softmax: lower values sharpen the distribution, while higher values flatten it and increase randomness.
- Top-K sampling restricts selection to a fixed number of highest-probability tokens, which can be too broad for peaked distributions and too narrow for diffuse ones.
- Top-P, or nucleus sampling, keeps the smallest probability mass whose cumulative probability crosses a threshold, adapting candidate-set size to the current distribution.
- Sampling policy changes generation behavior without changing the Transformer architecture or serving memory layout.

## Related Pages

- [Autoregressive Generation](autoregressive-generation.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [探秘Transformer系列之（15）--- 采样和输出](../sources/cnblogs-transformer-series-15-sampling-and-output.md)
