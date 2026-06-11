# Wiki Index

This file is maintained by the agent.

## Sources

- [Efficient Memory Management for Large Language Model Serving with PagedAttention](sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md) - Paged KV-cache management paper behind vLLM that cuts fragmentation and raises effective serving batch size.
- [How Should We Learn Again When AI Defeats Exam-Oriented Education?](sources/how-should-we-learn-again-when-ai-defeats-exam-oriented-education.md) - Video interview on AI-native learning, brain-inspired AI, System 1/System 2 intelligence, and why memorization-heavy education loses value.
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
- [Self-Attention Mechanism Deep Dive](sources/self-attention-mechanism-deep-dive.md) - Detailed attention guide covering QKV roles, scaled dot-product attention, softmax stability, MQA/GQA/MLA, causal masking, and FlashAttention IO behavior.
- [3.4 Transformer前馈网络FFN深入理解](sources/transformer-ffn-deep-dive.md) - Chinese AI Infra Guide chapter on FFN structure, SwiGLU, parameter sizing, tensor parallel FFN splits, MoE experts, and FFN kernel fusion.
- [3.5 Transformer位置编码深入理解](sources/transformer-positional-encoding-deep-dive.md) - Chinese AI Infra Guide chapter on positional encoding, RoPE, ALiBi, long-context RoPE scaling, kernel fusion, and KV-cache implications.
- [3.6 LayerNorm与残差连接深入理解](sources/layernorm-and-residual-connections-deep-dive.md) - Chinese AI Infra Guide chapter on residual paths, LayerNorm, RMSNorm, Pre-Norm/Post-Norm, DeepNorm, and fused normalization kernels.
- [3.7 Transformer Decoder Block完整解析](sources/transformer-decoder-block-deep-dive.md) - Chinese AI Infra Guide chapter decomposing decoder-only blocks, causal masking, parameter/FLOPs formulas, and memory planning.
- [3.8 从Transformer到LLM自回归生成深入理解](sources/transformer-to-llm-autoregressive-generation.md) - Chinese AI Infra Guide chapter on autoregressive generation, sampling, prefill/decode, KV cache, PagedAttention, and serving metrics.
- [3.9 Tokenization与词嵌入](sources/tokenization-and-word-embedding.md) - Chinese AI Infra Guide chapter on tokenization, BPE, embeddings, vocabulary size, positional information, and weight tying.
- [Transformer and Attention, Explained Plainly](sources/transformer-and-attention-a-layman-guide.md) - Plain-language walkthrough of tokenization, attention, encoder/decoder structure, and autoregressive generation.
- [Transformer Architecture Quick Start](sources/transformer-architecture-quick-start.md) - Chinese infrastructure-oriented Transformer architecture guide connecting attention, FFN, RoPE, KV cache, tensor parallelism, and inference optimization.
- [Transformer Overview and Code Implementation](sources/transformer-overview-and-code-implementation.md) - Chinese full-map Transformer guide covering encoder-decoder structure, architecture variants, masks, tensor shapes, and a PyTorch implementation.
- [How to Generate Tokens Faster: A vLLM Performance Model](sources/vllm-performance-model.md) - Systems-modeling note that explains vLLM serving behavior through throughput, TTFT, queueing, and interference.
- [We're at AI's Halftime](sources/were-at-ais-halftime.md) - Essay arguing that AI progress is shifting from benchmark hillclimbing toward evaluation setups that better capture real utility.
- [Welcome to the Era of Experience](sources/welcome-to-the-era-of-experience.md) - Position paper arguing that future AI progress will come from long-horizon, grounded learning from experience.
- [The Geometry of Consolidation v6 (Paper)](sources/geometry-of-consolidation-v6.md) - NeurIPS 2026 paper proving the Consolidation-Interference Duality, with companion repository reproduction notes folded into the same source page.
- [Language Modeling Is Compression](sources/language-modeling-is-compression.md) - DeepMind paper showing LLMs as general-purpose compressors via the prediction-compression equivalence, with cross-modal compression results.
- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](sources/kv-cache-architecture-survey.md) - Comprehensive survey of KVCache optimization from MHA through sparse and linear attention, with concrete memory comparisons.
- [向量数据库 (Vector Database)](sources/vector-database-overview.md) - Chinese introductory article on vector databases, ANN algorithms, similarity measurement, and database selection.

## Topics

- [CUDA Programming](topics/cuda-programming.md) - Durable overview of CUDA execution, synchronization, and performance-sensitive design.
- [AI-Native Learning](topics/ai-native-learning.md) - Shift from memorization and exam drilling toward self-directed, first-principles, AI-assisted open-ended learning.
- [Disaggregated LLM Inference](topics/disaggregated-llm-inference.md) - Serving view that separates prefill and decode so each phase can be scheduled, provisioned, and cached on its own terms.
- [Experiential AI](topics/experiential-ai.md) - View of advanced agents as long-lived, grounded learners, plus the live dispute over human-derived priors, algorithms, evaluation, and reliability.
- [LLM Deployment and Capacity Planning](topics/llm-deployment-and-capacity-planning.md) - Operating view of model serving focused on memory planning, latency metrics, batching, and incident response.
- [Private Credit](topics/private-credit.md) - Non-bank lending market spanning direct lending, asset-based finance, and increasingly entangled funding channels.
- [Transformer Architecture and Attention](topics/transformer-architecture-and-attention.md) - Foundational model of tokenization, attention, mask semantics, RoPE, decoder-only blocks, KV cache, and serving optimization targets.
- [Embedding Memory Geometry](topics/embedding-memory-geometry.md) - Geometric study of semantic memory: effective dimension, consolidation limits, and the tight/spread phase boundary that determines centroid near-optimality on real text.
- [Compression and Language Models](topics/compression-and-language-models.md) - Prediction-compression equivalence, LLMs as general-purpose cross-modal compressors, and scaling-law insights from adjusted compression rates.
- [Vector Database and ANN Search](topics/vector-database-and-ann-search.md) - Vector databases for RAG and semantic search, covering ANN algorithms (K-Means, PQ, HNSW, LSH), similarity measures, and filtering strategies.

## Concepts

- [Attention Mechanism](concepts/attention-mechanism.md) - Q/K/V weighting operation behind self-attention, multi-head attention implementation, masking variants, FlashAttention, and KV cache.
- [Autoregressive Generation](concepts/autoregressive-generation.md) - Next-token generation loop that creates prefill/decode phases, KV-cache reuse, TTFT/TPOT trade-offs, and iteration-level scheduling needs.
- [Brain-Inspired AI](concepts/brain-inspired-ai.md) - Neuroscience-informed view that future AI may need richer neural complexity, long-range feedback, parallel perception, and embodied action loops.
- [Context Caching in LLM Serving](concepts/context-caching-in-llm-serving.md) - Reuse of prefix KV state across requests to reduce repeated prefill work.
- [CUDA Thread Hierarchy](concepts/cuda-thread-hierarchy.md) - The `Grid -> Block -> Thread` structure that defines CUDA work partitioning.
- [Grounded Rewards](concepts/grounded-rewards.md) - Environmental feedback signals used to optimize agent behavior beyond human prejudgement.
- [GPU Memory Hierarchy](concepts/gpu-memory-hierarchy.md) - The trade-offs among registers, shared memory, local memory, and global memory.
- [Integer-Only Quantization](concepts/integer-only-quantization.md) - Low-bit deployment approach that pairs scale and zero-point with integer arithmetic and quantization-aware training.
- [Iteration-Level Scheduling](concepts/iteration-level-scheduling.md) - Serving policy that re-forms batches after each generation step instead of at full-request granularity.
- [KV Cache in LLM Serving](concepts/kv-cache-in-llm-serving.md) - Why attention cache dominates variable inference memory and how to estimate it.
- [Model Bandwidth Utilization](concepts/model-bandwidth-utilization.md) - A normalized measure of how efficiently an inference stack uses available memory bandwidth.
- [PagedAttention](concepts/pagedattention.md) - Block-based KV-cache layout that trades contiguous allocation for much better utilization and sharing.
- [Parallelism in LLM Serving](concepts/parallelism-in-llm-serving.md) - Tensor/expert parallelism distinctions, including attention-head and FFN split points for Transformer serving.
- [Prefill-Decode Disaggregation](concepts/prefill-decode-disaggregation.md) - Separation of parallel prompt processing and sequential KV-cache-heavy token generation into different serving pools.
- [Rated Note Feeders](concepts/rated-note-feeders.md) - Structured wrappers that make private-credit exposure easier for regulated investors to hold.
- [Streams of Experience](concepts/streams-of-experience.md) - Long-lived action-observation trajectories that support adaptation and long-horizon optimization.
- [Unitranche Loans](concepts/unitranche-loans.md) - Single-loan structures that merge senior and junior debt to trade clarity for execution speed.
- [Utility Problem](concepts/utility-problem.md) - The gap between benchmark capability and durable real-world usefulness when evaluation setups miss how work actually happens.
- [Effective Dimension](concepts/effective-dimension.md) - Participation ratio measuring how many truly independent directions a cluster's covariance occupies; governs the Consolidation-Interference Duality bound.
- [Prediction-Compression Equivalence](concepts/prediction-compression-equivalence.md) - Information-theoretic bridge between probabilistic prediction, cross-entropy, and lossless compression.
- [Positional Encoding](concepts/positional-encoding.md) - Order signal for Transformers, covering absolute encodings, RoPE Q/K rotation, ALiBi score bias, and long-context scaling.
- [Multi-head Latent Attention (MLA)](concepts/multi-head-latent-attention-mla.md) - DeepSeek's attention variant that compresses KV state into a low-rank latent vector for ~96% KVCache reduction.
- [Tokenization and Embeddings](concepts/tokenization-and-embeddings.md) - Text-to-token and token-to-vector input layer, including subword tokenization, embedding tables, vocabulary memory, and weight tying.
- [Transformer Feed-Forward Network](concepts/transformer-feed-forward-network.md) - Per-token nonlinear Transformer sublayer covering standard FFN, SwiGLU, dense parameter share, tensor-parallel splits, and MoE expertization.
- [Transformer Normalization and Residuals](concepts/transformer-normalization-and-residuals.md) - Stability machinery for deep Transformer stacks: residual identity paths, LayerNorm/RMSNorm, Pre-Norm, and fused residual-norm kernels.
- [Product Quantization](concepts/product-quantization.md) - Vector compression by sub-vector quantization with learned codebooks, the backbone of billion-scale ANN search.
- [Hierarchical Navigable Small Worlds (HNSW)](concepts/hierarchical-navigable-small-worlds-hnsw.md) - Multi-layer graph-based ANN algorithm with top-down search from long-jump to dense-granularity layers.

## Synthesis

- [AI Halftime vs Bitter Lesson and Era of Experience](synthesis/ai-halftime-vs-bitter-lesson-and-era-of-experience.md) - Comparative analysis of the substantive but staged conflict over language priors, grounded experience, algorithms, and reliability.
