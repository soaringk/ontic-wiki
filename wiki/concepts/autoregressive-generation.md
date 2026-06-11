# Autoregressive Generation

Autoregressive generation produces text one token at a time, conditioning each new token on all prior tokens.

## Why It Matters

- Decoder-only LLMs model `P(x_t | x_<t)` and generate by repeatedly sampling the next token, appending it, and running the next step.
- The generation loop creates two serving phases: prefill processes the prompt in parallel and builds KV Cache, while decode reads the cache and emits one new token at a time.
- Prefill usually determines TTFT and is compute-bound for long prompts; decode usually determines TPOT and is memory-bandwidth-bound.
- Greedy decoding, temperature, Top-K, and Top-P are output-selection policies over logits, not architecture changes.
- KV Cache is the key optimization that prevents recomputing historical K/V projections at every decode step.
- Continuous batching and iteration-level scheduling are natural responses to autoregressive generation because requests enter and finish at different token steps.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Iteration-Level Scheduling](iteration-level-scheduling.md)
- [Prefill-Decode Disaggregation](prefill-decode-disaggregation.md)

## Sources

- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [3.7 Transformer Decoder Block完整解析](../sources/transformer-decoder-block-deep-dive.md)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](../sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md)
