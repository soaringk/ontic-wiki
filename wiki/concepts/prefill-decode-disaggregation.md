# Prefill-Decode Disaggregation

Prefill-decode disaggregation separates prompt processing from autoregressive token generation into different execution pools or instances.

## Why It Matters

- Prefill and decode usually want different hardware, batch sizes, and parallelism strategies.
- It removes direct contention between compute-heavy prompt work and memory-heavy decode work.
- It enables per-phase SLO tuning around TTFT and TPOT or TBT.
- It often increases goodput, but only if KV-cache transfer is fast enough.

## Main Trade-off

- The benefit comes from less interference and better specialization.
- The cost comes from model duplication, state transfer, placement complexity, and more operational machinery.

## Related Pages

- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- [Context Caching in LLM Serving](context-caching-in-llm-serving.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)

## Sources

- [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](../sources/splitwise-efficient-generative-llm-inference-using-phase-splitting.md)
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](../sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md)
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](../sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md)
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](../sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md)
