# Context Caching in LLM Serving

Context caching preserves reusable KV cache for prompt prefixes so later requests can skip recomputing shared context.

## Why It Matters

- It reduces repeated prefill work for system prompts, repeated documents, and long shared prefixes.
- It turns serving from a stateless request pipeline into a stateful cache-management system.
- It changes scheduler incentives because request routing now affects cache-hit rate.
- In disaggregated systems, useful cache reuse may require decode-to-prefill return paths and distributed indexing.

## Main Risks

- Remote cache fetches can erase gains if latency or congestion is too high.
- Cache policies, indexing granularity, and block popularity distribution can dominate observed benefit.

## Related Pages

- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Prefill-Decode Disaggregation](prefill-decode-disaggregation.md)
- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)

## Sources

- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](../sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md)
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](../sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
