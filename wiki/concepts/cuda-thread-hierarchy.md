# CUDA Thread Hierarchy

CUDA organizes execution as `Grid -> Block -> Thread`.

## What The Hierarchy Does

- A kernel launch creates one grid.
- A grid contains multiple blocks.
- A block contains multiple threads.
- Thread-local indices such as `threadIdx` are only unique inside a block, while `blockIdx` identifies the block inside the grid.

## Why It Matters

- It provides the mapping from logical work units to GPU execution.
- Blocks are the main unit of independence and scheduling across streaming multiprocessors.
- In-block collaboration is possible through synchronization and shared memory, but cross-block synchronization is not part of the basic execution model.
- Long-sequence attention kernels may need to expose parallel work over sequence blocks, not only batch and heads, to keep streaming multiprocessors occupied.
- Warp-level work partitioning matters: FlashAttention-2 reduces intra-block shared-memory communication by splitting Q across warps instead of using a split-K pattern.
- Hopper-era kernels can use warp specialization, separating producer warps for data movement from consumer warps for Tensor Core work.

## Performance Implications

- Block size affects occupancy because registers and shared memory are allocated per active block.
- Global thread IDs are usually derived from `blockIdx`, `blockDim`, and `threadIdx`.
- Thread layout can influence warp divergence and memory coalescing.

## Related Pages

- [CUDA Programming](../topics/cuda-programming.md)
- [GPU Memory Hierarchy](gpu-memory-hierarchy.md)
- [FlashAttention](flashattention.md)

## Sources

- [CUDA C Programming Introduction - Parallel Computing](../sources/cuda-c-programming-introduction-parallel-computing.md)
- [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](../sources/flashattention-2-faster-attention-with-better-parallelism-and-work-partitioning.md)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](../sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md)
