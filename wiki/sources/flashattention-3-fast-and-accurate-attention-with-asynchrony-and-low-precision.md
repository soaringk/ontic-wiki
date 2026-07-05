---
kind: source
title: "FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision"
slug: flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision
source_ids:
  - raw-2407-08608v2
status: active
raw_path: raw/2407.08608v2.pdf
source_type: pdf
parser: mineru
published: 2024-07-16
created: 2026-07-06
updated: 2026-07-06
---

# Summary

FlashAttention-3 redesigns FlashAttention for NVIDIA Hopper GPUs. It exploits asynchronous Tensor Core and Tensor Memory Accelerator behavior, overlaps softmax with blockwise GEMMs, and adds an FP8 forward path using block quantization and incoherent processing to reduce low-precision error.

# Key Claims

- FlashAttention-2 does not fully exploit Hopper hardware; the paper reports only about 35% H100 utilization compared with much higher GEMM utilization.
- Producer-consumer warp specialization uses separate warps for data movement and compute, with register reallocation and asynchronous TMA/WGMMA operations.
- Ping-pong and intra-warpgroup pipelining hide softmax work under asynchronous GEMMs, addressing non-matmul operations such as exponentials that can otherwise become visible bottlenecks.
- The FP8 path requires layout-aware handling of WGMMA operands and accumulators, including in-kernel transpose for V tiles.
- Block quantization and incoherent processing mitigate FP8 error from outlier features while preserving exact attention structure before quantization.
- Experiments report 1.5-2.0x FP16 speedup over FlashAttention-2 on H100, up to 740 TFLOPs/s, close to 1.2 PFLOPs/s with FP8, and 2.6x lower FP8 numerical error than a per-tensor quantization baseline.

# Why It Matters

FlashAttention-3 shifts the FlashAttention story from memory IO alone to hardware-generation-specific asynchrony and precision. It is a reminder that serving and training kernels must be evaluated against the actual accelerator execution model, not only algorithmic complexity.

# Connections

- Concept: [FlashAttention](../concepts/flashattention.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [GPU Memory Hierarchy](../concepts/gpu-memory-hierarchy.md)
- Concept: [CUDA Thread Hierarchy](../concepts/cuda-thread-hierarchy.md)
- Concept: [LLM Quantization](../concepts/llm-quantization.md)
- Topic: [CUDA Programming](../topics/cuda-programming.md)
- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

# Open Questions

- The paper flags inference optimization, persistent FP8 kernels, and large-scale training effects of low-precision attention as remaining work.
