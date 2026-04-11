# CUDA Programming

CUDA programming is the study of expressing work for NVIDIA GPUs in a way that matches the machine's execution and memory model. The durable theme across the current material is that correctness comes from understanding the host-device split and thread hierarchy, while performance comes from memory-aware and warp-aware implementation choices.

## Core Ideas

- CUDA treats GPU work as kernels launched from host code onto a `Grid -> Block -> Thread` hierarchy.
- Blocks are independent scheduling units; threads inside a block can synchronize and share memory.
- Kernel launch is asynchronous from the host perspective, so synchronization and memory transfers define when results become usable.
- Performance depends on occupancy, latency hiding, memory coalescing, and reducing warp divergence.

## Related Concepts

- [CUDA Thread Hierarchy](../concepts/cuda-thread-hierarchy.md)
- [GPU Memory Hierarchy](../concepts/gpu-memory-hierarchy.md)

## Sources

- [CUDA C Programming Introduction - Parallel Computing](../sources/cuda-c-programming-introduction-parallel-computing.md)
