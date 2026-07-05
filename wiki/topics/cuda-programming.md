# CUDA Programming

CUDA programming is the study of expressing work for NVIDIA GPUs in a way that matches the machine's execution and memory model. The durable theme across the current material is that correctness comes from understanding the host-device split and thread hierarchy, while performance comes from memory-aware and warp-aware implementation choices.

## Core Ideas

- CUDA treats GPU work as kernels launched from host code onto a `Grid -> Block -> Thread` hierarchy.
- Blocks are independent scheduling units; threads inside a block can synchronize and share memory.
- Kernel launch is asynchronous from the host perspective, so synchronization and memory transfers define when results become usable.
- Performance depends on occupancy, latency hiding, memory coalescing, and reducing warp divergence.
- Deep-learning kernels such as FlashAttention show why IO-aware design matters: fewer HBM transactions can beat lower-FLOP algorithms, and later GPU generations reward asynchronous data movement plus warp-specialized scheduling.

## Related Concepts

- [CUDA Thread Hierarchy](../concepts/cuda-thread-hierarchy.md)
- [GPU Memory Hierarchy](../concepts/gpu-memory-hierarchy.md)
- [FlashAttention](../concepts/flashattention.md)

## Sources

- [CUDA C Programming Introduction - Parallel Computing](../sources/cuda-c-programming-introduction-parallel-computing.md)
- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../sources/flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness.md)
- [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](../sources/flashattention-2-faster-attention-with-better-parallelism-and-work-partitioning.md)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](../sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md)
