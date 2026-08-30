# Speculative Decoding

Speculative decoding accelerates autoregressive generation by using a cheaper draft model or candidate-generation path to propose future tokens, then having the target model verify them in parallel. A smaller independent draft model is the canonical speculative-sampling design.

## Why It Matters

- Autoregressive generation is serial because each accepted token normally depends on the previous target-model step.
- A draft model can cheaply propose multiple candidate tokens, then the target model validates those candidates in one larger forward pass.
- Accepted draft tokens let the serving system produce more than one output token per target-model step, improving decode throughput when draft acceptance is high.
- Exact speculative sampling preserves the target model's output distribution; this guarantee does not automatically extend to every candidate-generation or verification variant.
- In exact speculative sampling, a draft token is accepted with probability `min(1, p/q)` under the target and draft probabilities; a rejected position is resampled from the normalized positive residual between those distributions.
- Lookahead length has a real trade-off: longer drafts reduce target calls only if enough later tokens are accepted, and they can increase latency variance.
- The method adds complexity: draft-model topology, acceptance rate, batching interaction, and memory overhead determine whether it improves real workloads.
- Other candidate-generation families such as Medusa, Lookahead, and multi-token prediction are compared on [Parallel Decoding Variants](parallel-decoding-variants.md).

## Related Pages

- [Autoregressive Generation](autoregressive-generation.md)
- [Parallel Decoding Variants](parallel-decoding-variants.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

## Sources

- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [Accelerating Large Language Model Decoding with Speculative Sampling](../sources/accelerating-large-language-model-decoding-with-speculative-sampling.md)
- [探秘Transformer系列之（30）--- 投机解码](../sources/cnblogs-transformer-series-30-speculative-decoding.md)
