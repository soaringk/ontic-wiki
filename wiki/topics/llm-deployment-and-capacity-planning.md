# LLM Deployment and Capacity Planning

LLM deployment and capacity planning sits between model architecture and production operations. The current material emphasizes that reliable serving depends on correct GPU memory estimation, explicit performance targets, batching policy, and fast operational responses when resource pressure shows up in latency or error rates.

## Core Ideas

- Deployment variants should separate public production models from test-only configurations.
- Memory planning is not just parameter count; it includes runtime reservation, hardware reservation, and KV cache.
- Decoder Block memory planning should be component-wise: embeddings and LM head scale with vocabulary, FFN dominates dense block parameters, attention KV state scales with KV head count, and optimizer/activation memory only applies to training.
- User experience depends on separating TTFT, TPOT, overall latency, and throughput instead of collapsing them into one metric.
- Decode speed is often constrained by memory bandwidth, so hardware bandwidth and serving-stack efficiency matter as much as raw compute.
- Autoregressive serving separates prefill, which builds the initial KV Cache and often controls TTFT, from decode, which repeatedly reads weights and KV state and often controls TPOT.
- Continuous batching is usually the right default for shared online serving, while static batching can still win for offline workloads.
- Request-level scheduling is a poor fit for autoregressive generation; iteration-level control is the more durable systems model.
- Token-budgeted scheduling matters because forward-pass latency follows total tokens more than request count, and long prefills can create visible generation stalls if admitted without bounds.
- Prefill and decode often want different batch sizes, parallelism strategies, and sometimes different hardware entirely.
- Chunked prefill and stall-free batching are deployment levers for colocated serving when full prefill/decode disaggregation is too costly or operationally complex.
- Speculative decoding can improve decode throughput by verifying draft tokens in parallel, but capacity planning should treat draft-model topology, acceptance rate, lookahead length, tail latency, and batching effects as workload-dependent variables.
- Medusa, Lookahead decoding, and multi-token prediction are related parallel-decoding variants; they shift work into candidate generation or auxiliary heads and still require verification, cache support, and workload-specific acceptance analysis.
- Prefix reuse, cache placement, and KV-state transfer are now first-class deployment concerns rather than narrow engine details.
- MoE deployments require explicit reasoning about what tensor parallelism splits and what expert parallelism splits.
- LoRA adapters and QLoRA-style low-bit fine-tuning reduce customization cost, but serving must account for adapter loading, merging, batching compatibility, and quantized-base quality.
- More GPUs and higher tensor parallelism usually improve fit and latency only sub-linearly because communication overhead and utilization losses rise.
- Quantization can reduce bandwidth and memory pressure, but it must be validated against model-quality regressions.
- Integer-only and quantization-aware approaches matter because real deployment wins come from arithmetic that hardware can execute efficiently, not only smaller checkpoint files.
- LLM quantization needs outlier-aware treatment of weights, activations, and KV cache; scheme names such as GPTQ, AWQ, SmoothQuant, and QLoRA are deployment candidates, not substitutes for quality and latency validation.
- Attention kernels are part of capacity planning: FlashAttention reduces activation memory and attention latency for long prompts, while FlashAttention-3 shows that Hopper/FP8 gains depend on asynchronous kernels and accuracy-aware quantization.
- Capacity incidents are often handled first through scaling or throttling rather than deep architectural changes.

## Related Concepts

- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- [Model Bandwidth Utilization](../concepts/model-bandwidth-utilization.md)
- [Parallelism in LLM Serving](../concepts/parallelism-in-llm-serving.md)
- [PagedAttention](../concepts/pagedattention.md)
- [Iteration-Level Scheduling](../concepts/iteration-level-scheduling.md)
- [Chunked Prefill Scheduling](../concepts/chunked-prefill-scheduling.md)
- [Prefill-Decode Disaggregation](../concepts/prefill-decode-disaggregation.md)
- [Autoregressive Generation](../concepts/autoregressive-generation.md)
- [Speculative Decoding](../concepts/speculative-decoding.md)
- [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- [Context Caching in LLM Serving](../concepts/context-caching-in-llm-serving.md)
- [Integer-Only Quantization](../concepts/integer-only-quantization.md)
- [Mixture of Experts](../concepts/mixture-of-experts.md)
- [Low-Rank Adaptation (LoRA)](../concepts/low-rank-adaptation-lora.md)
- [LLM Quantization](../concepts/llm-quantization.md)
- [Parallel Decoding Variants](../concepts/parallel-decoding-variants.md)
- [Long Context Extrapolation](../concepts/long-context-extrapolation.md)
- [FlashAttention](../concepts/flashattention.md)

## Sources

- [LLM Deployment Principles and Memory Estimation Cheat Sheet](../sources/llm-deployment-principles-and-memory-estimation.md)
- [LLM Inference Performance Engineering Best Practices](../sources/llm-inference-performance-engineering-best-practices.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](../sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md)
- [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](../sources/splitwise-efficient-generative-llm-inference-using-phase-splitting.md)
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](../sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md)
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](../sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md)
- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](../sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md)
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](../sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md)
- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](../sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md)
- [How to Generate Tokens Faster: A vLLM Performance Model](../sources/vllm-performance-model.md)
- [3.7 Transformer Decoder Block完整解析](../sources/transformer-decoder-block-deep-dive.md)
- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [Accelerating Large Language Model Decoding with Speculative Sampling](../sources/accelerating-large-language-model-decoding-with-speculative-sampling.md)
- [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](../sources/deepspeed-fastgen-high-throughput-text-generation-for-llms.md)
- [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](../sources/taming-throughput-latency-tradeoff-in-llm-inference-with-sarathi-serve.md)
- [探秘Transformer系列之（16）--- 资源占用](../sources/cnblogs-transformer-series-16-resource-usage.md)
- [探秘Transformer系列之（20）--- KV Cache](../sources/cnblogs-transformer-series-20-kv-cache.md)
- [探秘Transformer系列之（22）--- LoRA](../sources/cnblogs-transformer-series-22-lora.md)
- [探秘Transformer系列之（26）--- KV Cache优化---分离or合并](../sources/cnblogs-transformer-series-26-kv-cache-split-or-merge.md)
- [探秘Transformer系列之（30）--- 投机解码](../sources/cnblogs-transformer-series-30-speculative-decoding.md)
- [探秘Transformer系列之（36）--- 大模型量化方案](../sources/cnblogs-transformer-series-36-llm-quantization-methods.md)
- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../sources/flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness.md)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](../sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md)
