# Speculative Decoding

Speculative decoding accelerates autoregressive generation by letting a smaller draft model propose several future tokens and having the target model verify them in parallel.

## Why It Matters

- Autoregressive generation is serial because each accepted token normally depends on the previous target-model step.
- A draft model can cheaply propose multiple candidate tokens, then the target model validates those candidates in one larger forward pass.
- Accepted draft tokens let the serving system produce more than one output token per target-model step, improving decode throughput when draft acceptance is high.
- Correct speculative decoding preserves the target model's output distribution; the speedup should not come from silently changing generation quality.
- A rejection or repair step is required: accepted draft tokens follow the target/draft probability ratio, while rejected positions are resampled from the positive residual between target and draft distributions.
- Lookahead length has a real trade-off: longer drafts reduce target calls only if enough later tokens are accepted, and they can increase latency variance.
- The method adds complexity: draft-model topology, acceptance rate, batching interaction, and memory overhead determine whether it improves real workloads.

## Related Pages

- [Autoregressive Generation](autoregressive-generation.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

## Sources

- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [Accelerating Large Language Model Decoding with Speculative Sampling](../sources/accelerating-large-language-model-decoding-with-speculative-sampling.md)
