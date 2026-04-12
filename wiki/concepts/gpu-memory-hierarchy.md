# GPU Memory Hierarchy

CUDA performance depends strongly on choosing the right memory level for the job.

## Main Levels

- Registers are thread-private and fastest, but scarce.
- Local memory is thread-private spill or array storage backed by device memory and cache.
- Shared memory is block-scoped and programmer-managed, making it the main tool for fast intra-block data reuse.
- Global memory is large and flexible but high latency.
- Constant and texture memory provide specialized read paths for favorable access patterns.

## Durable Lessons

- Reuse hot data in shared memory when that reduces repeated global-memory traffic.
- Keep global accesses aligned and coalesced across the warp.
- Structure-of-arrays layouts are often friendlier to GPU access patterns than array-of-structures layouts.
- More shared memory or registers can improve local efficiency but also reduce occupancy.

## Related Pages

- [CUDA Programming](../topics/cuda-programming.md)
- [CUDA Thread Hierarchy](cuda-thread-hierarchy.md)

## Sources

- [CUDA C Programming Introduction - Parallel Computing](../sources/cuda-c-programming-introduction-parallel-computing.md)
