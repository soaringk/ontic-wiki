# Wiki Index

This file is maintained by the agent.

## Sources

- [CUDA C Programming Introduction - Parallel Computing](sources/cuda-c-programming-introduction-parallel-computing.md) - Introductory CUDA notes on the host-device model, thread hierarchy, and memory-aware performance.
- [LLM Deployment Principles and Memory Estimation Cheat Sheet](sources/llm-deployment-principles-and-memory-estimation.md) - Deployment notes covering redundancy, GPU memory estimation, KV cache sizing, and first-response recovery.
- [Welcome to the Era of Experience](sources/welcome-to-the-era-of-experience.md) - Position paper arguing that future AI progress will come from long-horizon, grounded learning from experience.

## Topics

- [CUDA Programming](topics/cuda-programming.md) - Durable overview of CUDA execution, synchronization, and performance-sensitive design.
- [Experiential AI](topics/experiential-ai.md) - View of advanced agents as long-lived, grounded learners driven by experience rather than only human data.
- [LLM Deployment and Capacity Planning](topics/llm-deployment-and-capacity-planning.md) - Operating view of model serving focused on memory planning and incident response.

## Concepts

- [CUDA Thread Hierarchy](concepts/cuda-thread-hierarchy.md) - The `Grid -> Block -> Thread` structure that defines CUDA work partitioning.
- [Grounded Rewards](concepts/grounded-rewards.md) - Environmental feedback signals used to optimize agent behavior beyond human prejudgement.
- [GPU Memory Hierarchy](concepts/gpu-memory-hierarchy.md) - The trade-offs among registers, shared memory, local memory, and global memory.
- [KV Cache in LLM Serving](concepts/kv-cache-in-llm-serving.md) - Why attention cache dominates variable inference memory and how to estimate it.
- [Parallelism in LLM Serving](concepts/parallelism-in-llm-serving.md) - The difference between tensor and expert parallelism when sizing MoE deployments.
- [Streams of Experience](concepts/streams-of-experience.md) - Long-lived action-observation trajectories that support adaptation and long-horizon optimization.

## Synthesis

No synthesis pages yet.
