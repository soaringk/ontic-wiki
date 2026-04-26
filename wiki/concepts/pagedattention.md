# PagedAttention

PagedAttention is an attention implementation that stores a sequence's KV cache as fixed-size logical blocks mapped to physical blocks rather than as one contiguous tensor.

## Why It Matters

- It removes most external fragmentation and sharply limits internal fragmentation.
- It allows KV cache to grow on demand instead of reserving full maximum-length space up front.
- It makes prompt sharing, branching, and copy-on-write updates much cheaper.
- It raises the effective batch size ceiling by turning wasted memory into usable request capacity.

## Operational Consequence

- Memory layout becomes part of scheduling policy, not just a kernel detail.
- Network transfer can become a new bottleneck if the paged layout creates too many tiny transfers across disaggregated instances.

## Related Pages

- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)

## Sources

- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [How to Generate Tokens Faster: A vLLM Performance Model](../sources/vllm-performance-model.md)
- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](../sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md)
