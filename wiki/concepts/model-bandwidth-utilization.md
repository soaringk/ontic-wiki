# Model Bandwidth Utilization

Model Bandwidth Utilization (MBU) is a model-based estimate of how much of a device's peak memory bandwidth an LLM inference stack uses in memory-bound serving regimes.

## Definition

- MBU divides an estimated or profiler-measured memory-traffic rate by peak memory bandwidth.
- The source uses `(model parameter bytes + KV cache bytes) / TPOT` as a simplified traffic proxy; it does not count every implementation-dependent transfer.
- MBU is most informative during decode-heavy, small-batch inference where memory movement, not FLOPs, is the bottleneck.
- Attention decode is a common example: each step handles one new token while reading model weights and the accumulated KV cache, so memory traffic can dominate available arithmetic.
- Low arithmetic intensity in decode batches can leave compute slack; schedulers such as Sarathi-Serve exploit this by adding bounded prefill chunks without greatly increasing decode latency.

## Why It Matters

- It gives a normalized way to compare serving efficiency when the same traffic-accounting convention is used.
- It explains why a system can show poor token latency even when theoretical compute capacity looks high.
- It highlights that higher tensor parallelism can lower effective utilization by splitting work into smaller transfers and adding coordination overhead.

## Operational Use

- Use MBU to diagnose whether the next improvement should come from better batching, better kernels, different hardware, or fewer parallel shards.
- Pair MBU with user-facing metrics such as TTFT, TPOT, and throughput rather than treating it as a standalone success metric.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Parallelism in LLM Serving](parallelism-in-llm-serving.md)
- [Chunked Prefill Scheduling](chunked-prefill-scheduling.md)

## Sources

- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
- [Self-Attention Mechanism Deep Dive](../sources/self-attention-mechanism-deep-dive.md)
- [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](../sources/taming-throughput-latency-tradeoff-in-llm-inference-with-sarathi-serve.md)
