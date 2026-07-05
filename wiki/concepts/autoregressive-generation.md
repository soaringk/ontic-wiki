# Autoregressive Generation

Autoregressive generation produces text one token at a time, conditioning each new token on all prior tokens.

## Why It Matters

- Decoder-only LLMs model `P(x_t | x_<t)` and generate by repeatedly sampling the next token, appending it, and running the next step.
- The generation loop creates two serving phases: prefill processes the prompt in parallel and builds KV Cache, while decode reads the cache and emits one new token at a time.
- Prefill usually determines TTFT and is compute-bound for long prompts; decode usually determines TPOT and is memory-bandwidth-bound.
- Greedy decoding, temperature, Top-K, and Top-P are output-selection policies over logits, not architecture changes.
- KV Cache is the key optimization that prevents full-prefix recomputation: without cache, autoregressive attention sums full-prefix matrix attention to $O(N^3 d)$; with cache, single-query decode attention sums to $O(N^2 d)$.
- Continuous batching and iteration-level scheduling are natural responses to autoregressive generation because requests enter and finish at different token steps.
- Long prefills can interrupt the decode cadence in shared serving; chunked prefill scheduling keeps new prompt work within a per-iteration token budget.
- Speculative decoding targets the serial decode bottleneck by using draft tokens plus target-model verification; its benefit depends on acceptance rate, lookahead length, draft latency, target scoring latency, and workload shape.
- Medusa, Lookahead decoding, and multi-token prediction are adjacent attempts to generate or verify multiple future tokens before committing them to the output stream.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Token Sampling Strategies](token-sampling-strategies.md)
- [Iteration-Level Scheduling](iteration-level-scheduling.md)
- [Chunked Prefill Scheduling](chunked-prefill-scheduling.md)
- [Prefill-Decode Disaggregation](prefill-decode-disaggregation.md)
- [Speculative Decoding](speculative-decoding.md)
- [Parallel Decoding Variants](parallel-decoding-variants.md)

## Sources

- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [3.7 Transformer Decoder Block完整解析](../sources/transformer-decoder-block-deep-dive.md)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](../sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md)
- [Accelerating Large Language Model Decoding with Speculative Sampling](../sources/accelerating-large-language-model-decoding-with-speculative-sampling.md)
- [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](../sources/deepspeed-fastgen-high-throughput-text-generation-for-llms.md)
- [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](../sources/taming-throughput-latency-tradeoff-in-llm-inference-with-sarathi-serve.md)
- [探秘Transformer系列之（5）--- 训练&推理](../sources/cnblogs-transformer-series-05-training-and-inference.md)
- [探秘Transformer系列之（20）--- KV Cache](../sources/cnblogs-transformer-series-20-kv-cache.md)
- [探秘Transformer系列之（30）--- 投机解码](../sources/cnblogs-transformer-series-30-speculative-decoding.md)
- [探秘Transformer系列之（33）--- DeepSeek MTP](../sources/cnblogs-transformer-series-33-deepseek-mtp.md)
