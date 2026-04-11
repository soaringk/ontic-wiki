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

## Performance Implications

- Block size affects occupancy because registers and shared memory are allocated per active block.
- Global thread IDs are usually derived from `blockIdx`, `blockDim`, and `threadIdx`.
- Thread layout can influence warp divergence and memory coalescing.

## Sources

- [CUDA C Programming Introduction - Parallel Computing](../sources/cuda-c-programming-introduction-parallel-computing.md)
