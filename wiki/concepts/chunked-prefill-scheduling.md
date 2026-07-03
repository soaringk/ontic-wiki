# Chunked Prefill Scheduling

Chunked prefill scheduling splits prompt processing into smaller token-budgeted units and mixes those units with ongoing decode work instead of executing each prompt as one large prefill pass.

## Why It Matters

- Long prompts can otherwise stall streaming generation because a full prefill may take much longer than a decode step.
- A fixed or profiled token budget bounds per-iteration work, making TBT or TPOT more predictable under load.
- Hybrid batches can use arithmetic slack in memory-bound decode iterations while still avoiding large generation stalls.
- More uniform per-iteration compute can reduce pipeline-parallel bubbles when inference spans multiple pipeline stages.

## Trade-offs

- Smaller chunks protect decode latency but add overhead from repeated scheduling, kernel launches, and extra KV-cache reads for earlier chunks.
- Larger chunks improve prefill efficiency but can reintroduce tail-latency spikes and pipeline imbalance.
- Chunked scheduling mitigates prefill/decode interference inside a colocated system; it is not the same as physically disaggregating prefill and decode pools.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [Disaggregated LLM Inference](../topics/disaggregated-llm-inference.md)
- [Iteration-Level Scheduling](iteration-level-scheduling.md)
- [Prefill-Decode Disaggregation](prefill-decode-disaggregation.md)

## Sources

- [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](../sources/deepspeed-fastgen-high-throughput-text-generation-for-llms.md)
- [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](../sources/taming-throughput-latency-tradeoff-in-llm-inference-with-sarathi-serve.md)
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](../sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md)
