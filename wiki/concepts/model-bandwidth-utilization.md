# Model Bandwidth Utilization

Model Bandwidth Utilization (MBU) measures how much of a device's peak memory bandwidth an LLM inference stack actually uses in memory-bound serving regimes.

## Definition

- MBU is the ratio of achieved memory bandwidth to peak memory bandwidth.
- The source approximates achieved bandwidth as `(model parameter bytes + KV cache bytes) / TPOT`.
- MBU is most informative during decode-heavy, small-batch inference where memory movement, not FLOPs, is the bottleneck.

## Why It Matters

- It gives a normalized way to compare serving efficiency across hardware and inference stacks.
- It explains why a system can show poor token latency even when theoretical compute capacity looks high.
- It highlights that higher tensor parallelism can lower effective utilization by splitting work into smaller transfers and adding coordination overhead.

## Operational Use

- Use MBU to diagnose whether the next improvement should come from better batching, better kernels, different hardware, or fewer parallel shards.
- Pair MBU with user-facing metrics such as TTFT, TPOT, and throughput rather than treating it as a standalone success metric.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Parallelism in LLM Serving](parallelism-in-llm-serving.md)

## Sources

- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
