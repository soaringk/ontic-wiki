# Disaggregated LLM Inference

Disaggregated LLM inference separates the prompt-processing and token-generation phases into different execution pools so each phase can be scheduled, parallelized, and provisioned for its own bottleneck. Across the current material, the recurring reason is that prefill is usually more compute-sensitive while decode is more memory-bandwidth- and KV-state-sensitive, so colocating them creates interference, coupled resource planning, and weaker SLO control.

## Core Ideas

- Prefill and decode expose different latency objectives: TTFT is mostly a prefill concern, while TPOT or TBT is mostly a decode concern.
- Mixed batching improves utilization in some cases, but it also creates cross-phase interference that can make both TTFT and decode latency worse.
- Disaggregation lets each phase choose different hardware, batch sizes, and parallelism strategies.
- KV cache becomes the central systems object because phase separation only works if the cache can be moved, reused, or reconstructed efficiently.
- Once KV cache persists across requests, context caching and disaggregation stop being separate features and start becoming one state-management problem.
- Good deployment decisions depend on workload shape, interconnect bandwidth, cache-hit structure, and overload behavior, not only raw tokens-per-second.

## Main Tensions

- Disaggregation removes interference but adds transfer overhead and operational complexity.
- Chunked prefill can partially mitigate interference inside a colocated system, but it does not fully remove the trade-off.
- Some systems optimize for goodput under SLOs, while others emphasize throughput per dollar, throughput per watt, or job completion time.
- Cache reuse can lower compute cost, but remote cache fetches can still hurt TTFT if they are too slow or too contended.

## Related Concepts

- [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- [PagedAttention](../concepts/pagedattention.md)

## Sources

- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](../sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md)
- [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](../sources/splitwise-efficient-generative-llm-inference-using-phase-splitting.md)
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](../sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md)
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](../sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md)
- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](../sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md)
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](../sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md)
- [How to Generate Tokens Faster: A vLLM Performance Model](../sources/vllm-performance-model.md)
