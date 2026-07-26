# Prefill-Decode Disaggregation

Prefill-decode disaggregation separates prompt processing from autoregressive token generation into different execution pools or instances.

## Why It Matters

- Prefill processes prompt tokens in parallel and builds KV state; decode adds one token at a time and repeatedly reads that state.
- Separating the phases enables specialized scheduling and provisioning, but only works when KV-cache transfer is fast enough for the workload's latency targets.

## Main Trade-off

- The benefit is reduced cross-phase interference and better specialization; the cost is model duplication, state transfer, placement complexity, and additional operational machinery.
- See [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md) for scheduler alternatives, workload considerations, and the broader source comparison.

## Related Pages

- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)

## Sources

- [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](../sources/splitwise-efficient-generative-llm-inference-using-phase-splitting.md)
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](../sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md)
