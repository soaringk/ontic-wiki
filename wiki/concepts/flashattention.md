# FlashAttention

FlashAttention is a family of exact attention kernels that make dense Transformer attention practical at longer sequence lengths by matching the algorithm to GPU memory hierarchy, thread scheduling, and accelerator-specific execution features.

## Core Ideas

- Standard attention materializes `QK^T` and the softmax probability matrix in HBM; FlashAttention avoids those `n x n` intermediate writes while preserving exact dense attention semantics.
- The original FlashAttention uses tiling, online softmax, and backward recomputation to reduce HBM traffic and activation memory from quadratic to linear in sequence length, while time remains quadratic for dense attention.
- Online softmax carries row-wise max and normalization statistics across blocks so blockwise softmax produces the same result as full-row softmax.
- FlashAttention-2 improves utilization after the IO bottleneck is reduced: it cuts non-matmul work, parallelizes over sequence blocks, and repartitions work between warps to reduce shared-memory communication.
- FlashAttention-3 targets Hopper GPUs by using asynchronous TMA/WGMMA execution, producer-consumer warp specialization, GEMM-softmax pipelining, and FP8 paths with block quantization plus incoherent processing.
- FlashAttention benefits MHA, MQA, GQA, MLA, sparse attention, and distributed attention because those variants still depend on efficient `softmax(QK^T)V` or closely related primitives.

## Version Progression

- FlashAttention V1: IO-aware exact attention using SRAM tiling and recomputation.
- FlashAttention-2: better parallelism, occupancy, and warp work partitioning on A100-class GPUs.
- FlashAttention-3: Hopper-specific asynchrony and low-precision support, including FP8 accuracy controls.

## Related Pages

- [Attention Mechanism](attention-mechanism.md)
- [GPU Memory Hierarchy](gpu-memory-hierarchy.md)
- [CUDA Thread Hierarchy](cuda-thread-hierarchy.md)
- [LLM Quantization](llm-quantization.md)
- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [CUDA Programming](../topics/cuda-programming.md)

## Sources

- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../sources/flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness.md)
- [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](../sources/flashattention-2-faster-attention-with-better-parallelism-and-work-partitioning.md)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](../sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md)
- [探秘Transformer系列之（18）--- FlashAttention](../sources/cnblogs-transformer-series-18-flashattention.md)
- [探秘Transformer系列之（19）----FlashAttention V2 及升级版本](../sources/cnblogs-transformer-series-19-flashattention-v2-and-beyond.md)
