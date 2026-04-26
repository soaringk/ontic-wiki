# Wiki Index

This file is maintained by the agent.

## Sources

- [Efficient Memory Management for Large Language Model Serving with PagedAttention](sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md) - Paged KV-cache management paper behind vLLM that cuts fragmentation and raises effective serving batch size.
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md) - Mixed-workload serving paper that combines disaggregation, chunked prefill, and length-aware decode scheduling.
- [The Bitter Lesson](sources/the-bitter-lesson.md) - Classic argument that scalable general methods using search, learning, and compute beat hand-built human knowledge in the long run.
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md) - Goodput-oriented serving design that separates prefill and decode to satisfy TTFT and TPOT together.
- [CUDA C Programming Introduction - Parallel Computing](sources/cuda-c-programming-introduction-parallel-computing.md) - Introductory CUDA notes on the host-device model, thread hierarchy, and memory-aware performance.
- [LLM Inference Performance Engineering Best Practices](sources/llm-inference-performance-engineering-best-practices.md) - Serving guide covering TTFT/TPOT, batching, memory-bandwidth limits, and hardware trade-offs.
- [LLM Deployment Principles and Memory Estimation Cheat Sheet](sources/llm-deployment-principles-and-memory-estimation.md) - Deployment notes covering redundancy, GPU memory estimation, KV cache sizing, and first-response recovery.
- [MemServe: Flexible Mem Pool for Building Disaggregated LLM Serving with Caching](sources/memserve-flexible-mem-pool-for-building-disaggregated-llm-serving-with-caching.md) - Memory-substrate design that combines context caching and disaggregated serving around distributed KV management.
- [Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving](sources/mooncake-a-kvcache-centric-disaggregated-architecture-for-llm-serving.md) - Production-oriented serving design centered on KV reuse, lower-tier cache pools, and overload-aware scheduling.
- [Orca: A Distributed Serving System for Transformer-Based Generative Models](sources/orca-a-distributed-serving-system-for-transformer-based-generative-models.md) - Early serving system that established iteration-level scheduling and selective batching for autoregressive generation.
- [Private Credit Podcast](sources/private-credit-podcast.md) - Long-form market analysis of private credit, its growth drivers, structures, and systemic-risk concerns.
- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md) - Quantization-aware training paper for practical integer-only inference on real hardware.
- [Splitwise: Efficient Generative LLM Inference Using Phase Splitting](sources/splitwise-efficient-generative-llm-inference-using-phase-splitting.md) - Phase-splitting paper that maps compute-heavy prefill and memory-bound decode onto different hardware pools.
- [Two Lessons from ICLR 2025](sources/two-lessons-from-iclr-2025.md) - Methodological critique that anchors AI progress in near-100%-reliable capabilities rather than hype and speculative roadmaps.
- [Transformer and Attention, Explained Plainly](sources/transformer-and-attention-a-layman-guide.md) - Plain-language walkthrough of tokenization, attention, encoder/decoder structure, and autoregressive generation.
- [How to Generate Tokens Faster: A vLLM Performance Model](sources/vllm-performance-model.md) - Systems-modeling note that explains vLLM serving behavior through throughput, TTFT, queueing, and interference.
- [We're at AI's Halftime](sources/were-at-ais-halftime.md) - Essay arguing that AI progress is shifting from benchmark hillclimbing toward evaluation setups that better capture real utility.
- [Welcome to the Era of Experience](sources/welcome-to-the-era-of-experience.md) - Position paper arguing that future AI progress will come from long-horizon, grounded learning from experience.

## Topics

- [CUDA Programming](topics/cuda-programming.md) - Durable overview of CUDA execution, synchronization, and performance-sensitive design.
- [Disaggregated LLM Inference](topics/disaggregated-llm-inference.md) - Serving view that separates prefill and decode so each phase can be scheduled, provisioned, and cached on its own terms.
- [Experiential AI](topics/experiential-ai.md) - View of advanced agents as long-lived, grounded learners, plus the live dispute over human-derived priors, algorithms, evaluation, and reliability.
- [LLM Deployment and Capacity Planning](topics/llm-deployment-and-capacity-planning.md) - Operating view of model serving focused on memory planning, latency metrics, batching, and incident response.
- [Private Credit](topics/private-credit.md) - Non-bank lending market spanning direct lending, asset-based finance, and increasingly entangled funding channels.
- [Transformer Architecture and Attention](topics/transformer-architecture-and-attention.md) - Foundational model of tokenization, attention, causal masking, and why decoder-only serving creates KV cache.

## Concepts

- [Attention Mechanism](concepts/attention-mechanism.md) - The context-dependent weighting operation that lets each token gather information from other tokens.
- [Context Caching in LLM Serving](concepts/context-caching-in-llm-serving.md) - Reuse of prefix KV state across requests to reduce repeated prefill work.
- [CUDA Thread Hierarchy](concepts/cuda-thread-hierarchy.md) - The `Grid -> Block -> Thread` structure that defines CUDA work partitioning.
- [Grounded Rewards](concepts/grounded-rewards.md) - Environmental feedback signals used to optimize agent behavior beyond human prejudgement.
- [GPU Memory Hierarchy](concepts/gpu-memory-hierarchy.md) - The trade-offs among registers, shared memory, local memory, and global memory.
- [Integer-Only Quantization](concepts/integer-only-quantization.md) - Low-bit deployment approach that pairs scale and zero-point with integer arithmetic and quantization-aware training.
- [Iteration-Level Scheduling](concepts/iteration-level-scheduling.md) - Serving policy that re-forms batches after each generation step instead of at full-request granularity.
- [KV Cache in LLM Serving](concepts/kv-cache-in-llm-serving.md) - Why attention cache dominates variable inference memory and how to estimate it.
- [Model Bandwidth Utilization](concepts/model-bandwidth-utilization.md) - A normalized measure of how efficiently an inference stack uses available memory bandwidth.
- [PagedAttention](concepts/pagedattention.md) - Block-based KV-cache layout that trades contiguous allocation for much better utilization and sharing.
- [Parallelism in LLM Serving](concepts/parallelism-in-llm-serving.md) - The difference between tensor and expert parallelism when sizing MoE deployments.
- [Prefill-Decode Disaggregation](concepts/prefill-decode-disaggregation.md) - Separation of prompt processing and token generation into different serving pools.
- [Rated Note Feeders](concepts/rated-note-feeders.md) - Structured wrappers that make private-credit exposure easier for regulated investors to hold.
- [Streams of Experience](concepts/streams-of-experience.md) - Long-lived action-observation trajectories that support adaptation and long-horizon optimization.
- [Unitranche Loans](concepts/unitranche-loans.md) - Single-loan structures that merge senior and junior debt to trade clarity for execution speed.
- [Utility Problem](concepts/utility-problem.md) - The gap between benchmark capability and durable real-world usefulness when evaluation setups miss how work actually happens.

## Synthesis

- [AI Halftime vs Bitter Lesson and Era of Experience](synthesis/ai-halftime-vs-bitter-lesson-and-era-of-experience.md) - Comparative analysis of the substantive but staged conflict over language priors, grounded experience, algorithms, and reliability.
