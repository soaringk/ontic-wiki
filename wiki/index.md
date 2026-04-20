# Wiki Index

This file is maintained by the agent.

## Sources

- [The Bitter Lesson](sources/the-bitter-lesson.md) - Classic argument that scalable general methods using search, learning, and compute beat hand-built human knowledge in the long run.
- [CUDA C Programming Introduction - Parallel Computing](sources/cuda-c-programming-introduction-parallel-computing.md) - Introductory CUDA notes on the host-device model, thread hierarchy, and memory-aware performance.
- [LLM Inference Performance Engineering Best Practices](sources/llm-inference-performance-engineering-best-practices.md) - Serving guide covering TTFT/TPOT, batching, memory-bandwidth limits, and hardware trade-offs.
- [LLM Deployment Principles and Memory Estimation Cheat Sheet](sources/llm-deployment-principles-and-memory-estimation.md) - Deployment notes covering redundancy, GPU memory estimation, KV cache sizing, and first-response recovery.
- [Private Credit Podcast](sources/private-credit-podcast.md) - Long-form market analysis of private credit, its growth drivers, structures, and systemic-risk concerns.
- [Two Lessons from ICLR 2025](sources/two-lessons-from-iclr-2025.md) - Methodological critique that anchors AI progress in near-100%-reliable capabilities rather than hype and speculative roadmaps.
- [We're at AI's Halftime](sources/were-at-ais-halftime.md) - Essay arguing that AI progress is shifting from benchmark hillclimbing toward evaluation setups that better capture real utility.
- [Welcome to the Era of Experience](sources/welcome-to-the-era-of-experience.md) - Position paper arguing that future AI progress will come from long-horizon, grounded learning from experience.

## Topics

- [CUDA Programming](topics/cuda-programming.md) - Durable overview of CUDA execution, synchronization, and performance-sensitive design.
- [Experiential AI](topics/experiential-ai.md) - View of advanced agents as long-lived, grounded learners, plus the live dispute over human-derived priors, algorithms, evaluation, and reliability.
- [LLM Deployment and Capacity Planning](topics/llm-deployment-and-capacity-planning.md) - Operating view of model serving focused on memory planning, latency metrics, batching, and incident response.
- [Private Credit](topics/private-credit.md) - Non-bank lending market spanning direct lending, asset-based finance, and increasingly entangled funding channels.

## Concepts

- [CUDA Thread Hierarchy](concepts/cuda-thread-hierarchy.md) - The `Grid -> Block -> Thread` structure that defines CUDA work partitioning.
- [Grounded Rewards](concepts/grounded-rewards.md) - Environmental feedback signals used to optimize agent behavior beyond human prejudgement.
- [GPU Memory Hierarchy](concepts/gpu-memory-hierarchy.md) - The trade-offs among registers, shared memory, local memory, and global memory.
- [KV Cache in LLM Serving](concepts/kv-cache-in-llm-serving.md) - Why attention cache dominates variable inference memory and how to estimate it.
- [Model Bandwidth Utilization](concepts/model-bandwidth-utilization.md) - A normalized measure of how efficiently an inference stack uses available memory bandwidth.
- [Parallelism in LLM Serving](concepts/parallelism-in-llm-serving.md) - The difference between tensor and expert parallelism when sizing MoE deployments.
- [Rated Note Feeders](concepts/rated-note-feeders.md) - Structured wrappers that make private-credit exposure easier for regulated investors to hold.
- [Streams of Experience](concepts/streams-of-experience.md) - Long-lived action-observation trajectories that support adaptation and long-horizon optimization.
- [Unitranche Loans](concepts/unitranche-loans.md) - Single-loan structures that merge senior and junior debt to trade clarity for execution speed.
- [Utility Problem](concepts/utility-problem.md) - The gap between benchmark capability and durable real-world usefulness when evaluation setups miss how work actually happens.

## Synthesis

- [AI Halftime vs Bitter Lesson and Era of Experience](synthesis/ai-halftime-vs-bitter-lesson-and-era-of-experience.md) - Comparative analysis separating hand-built knowledge, learned language priors, and human-data ceilings in the current AI-progress debate.
