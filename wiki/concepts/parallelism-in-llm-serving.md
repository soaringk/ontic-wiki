# Parallelism in LLM Serving

Serving large models requires separating which parts of the model are split by tensor parallelism and which are split by expert parallelism.

## Main Distinction

- Tensor parallelism (TP) usually slices weights across devices for dense layers and attention-related tensors.
- Expert parallelism (EP) is mainly relevant for MoE routed experts.
- Shared experts and dense prefixes may still follow TP-style partitioning even when routed experts use EP.
- Increasing TP can reduce first-token and decode latency, but gains diminish as communication and utilization costs rise.

## Why It Matters

- Wrong assumptions about TP versus EP lead directly to wrong GPU memory estimates.
- Capacity planning for MoE models must reason about dense layers, shared experts, and routed experts separately.
- Smaller models can lose memory-bandwidth efficiency when spread too aggressively across GPUs.

## Operational Consequence

- Memory formulas should be checked component by component rather than with a single global parameter-count estimate.
- Hardware topology matters: the same GPU count can behave differently depending on interconnect bandwidth and layout.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Model Bandwidth Utilization](model-bandwidth-utilization.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
