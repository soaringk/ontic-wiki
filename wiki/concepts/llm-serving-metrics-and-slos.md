# LLM Serving Metrics and SLOs

LLM serving must be measured as a latency-throughput system rather than by one aggregate speed number.

## Core Metrics

- **Time to first token (TTFT)** covers queueing plus prompt prefill before streaming begins.
- **Time per output token (TPOT), or time between tokens (TBT),** describes decode cadence after the first token.
- **End-to-end latency** covers the request's full queueing and service time.
- **Throughput** measures completed requests or processed tokens per unit time without requiring latency targets to be met.
- **Goodput** measures the request rate that satisfies defined latency SLOs; the cited DistServe source evaluates it under both TTFT and TPOT constraints.

## Operating Implications

- Queueing delay rises sharply near saturation, so peak throughput can produce poor user-visible latency.
- Prefill and decode stress hardware differently, which can put TTFT and TPOT in tension under shared batching.
- Metric definitions, percentiles, request-length distributions, and SLO thresholds must be stated for comparisons to be meaningful.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- [Autoregressive Generation](autoregressive-generation.md)
- [Iteration-Level Scheduling](iteration-level-scheduling.md)

## Sources

- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](../sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md)
- [How to Generate Tokens Faster: A vLLM Performance Model](../sources/vllm-performance-model.md)
