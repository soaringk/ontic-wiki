# Wiki Index

This file is maintained by the agent.

## Sources

- [Efficient Memory Management for Large Language Model Serving with PagedAttention](sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md) - Paged KV-cache management paper behind vLLM that cuts fragmentation and raises effective serving batch size.
- [Accelerating Large Language Model Decoding with Speculative Sampling](sources/accelerating-large-language-model-decoding-with-speculative-sampling.md) - DeepMind speculative sampling paper that uses draft-model proposals plus target-model rejection sampling to speed decode while preserving the target distribution.
- [DeepSpeed-FastGen: High-throughput Text Generation for LLMs via MII and DeepSpeed-Inference](sources/deepspeed-fastgen-high-throughput-text-generation-for-llms.md) - DeepSpeed serving paper introducing Dynamic SplitFuse to compose prompt and generation tokens into consistent token-budgeted forward passes.
- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](sources/flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness.md) - IO-aware exact attention paper using tiling, online softmax, and recomputation to avoid materializing the quadratic attention matrix.
- [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](sources/flashattention-2-faster-attention-with-better-parallelism-and-work-partitioning.md) - Follow-up kernel paper improving FlashAttention through reduced non-matmul work, sequence-block parallelism, and warp work partitioning.
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md) - Hopper-focused FlashAttention paper using TMA/WGMMA asynchrony, GEMM-softmax overlap, and FP8 block quantization.
- [How Should We Learn Again When AI Defeats Exam-Oriented Education?](sources/how-should-we-learn-again-when-ai-defeats-exam-oriented-education.md) - Video interview on AI-native learning, brain-inspired AI, System 1/System 2 intelligence, and why memorization-heavy education loses value.
- [Inference without Interference: Disaggregate LLM Inference for Mixed Downstream Workloads](sources/inference-without-interference-disaggregate-llm-inference-for-mixed-downstream-workloads.md) - Mixed-workload serving paper that combines disaggregation, chunked prefill, and length-aware decode scheduling.
- [The Bitter Lesson](sources/the-bitter-lesson.md) - Classic argument that scalable general methods using search, learning, and compute beat hand-built human knowledge in the long run.
- [DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving](sources/distserve-disaggregating-prefill-and-decoding-for-goodput-optimized-large-language-model-serving.md) - Goodput-oriented serving design that separates prefill and decode to satisfy TTFT and TPOT together.
- [Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve](sources/taming-throughput-latency-tradeoff-in-llm-inference-with-sarathi-serve.md) - Scheduler paper using chunked prefills and stall-free batching to reduce generation stalls while preserving serving capacity.
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
- [Self-attention Does Not Need O(n^2) Memory](sources/self-attention-does-not-need-o-n2-memory.md) - Exact memory-efficient attention paper separating quadratic attention time from avoidable quadratic attention-matrix memory.
- [3.4 Transformer前馈网络FFN深入理解](sources/transformer-ffn-deep-dive.md) - Chinese AI Infra Guide chapter on FFN structure, SwiGLU, parameter sizing, tensor parallel FFN splits, MoE experts, and FFN kernel fusion.
- [3.5 Transformer位置编码深入理解](sources/transformer-positional-encoding-deep-dive.md) - Chinese AI Infra Guide chapter on positional encoding, RoPE, ALiBi, long-context RoPE scaling, kernel fusion, and KV-cache implications.
- [3.6 LayerNorm与残差连接深入理解](sources/layernorm-and-residual-connections-deep-dive.md) - Chinese AI Infra Guide chapter on residual paths, LayerNorm, RMSNorm, Pre-Norm/Post-Norm, DeepNorm, and fused normalization kernels.
- [3.7 Transformer Decoder Block完整解析](sources/transformer-decoder-block-deep-dive.md) - Chinese AI Infra Guide chapter decomposing decoder-only blocks, causal masking, parameter/FLOPs formulas, and memory planning.
- [3.8 从Transformer到LLM自回归生成深入理解](sources/transformer-to-llm-autoregressive-generation.md) - Chinese AI Infra Guide chapter on autoregressive generation, sampling, prefill/decode, KV cache, PagedAttention, speculative decoding, and serving metrics.
- [3.9 Tokenization与词嵌入](sources/tokenization-and-word-embedding.md) - Chinese AI Infra Guide chapter on tokenization, BPE, embeddings, vocabulary size, positional information, and weight tying.
- [Transformer and Attention, Explained Plainly](sources/transformer-and-attention-a-layman-guide.md) - Plain-language walkthrough of tokenization, attention, encoder/decoder structure, and autoregressive generation.
- [Transformer Architecture Quick Start](sources/transformer-architecture-quick-start.md) - Chinese infrastructure-oriented Transformer architecture guide connecting attention, FFN, RoPE, KV cache, tensor parallelism, and inference optimization.
- [Transformer Overview and Code Implementation](sources/transformer-overview-and-code-implementation.md) - Chinese full-map Transformer guide covering encoder-decoder structure, architecture variants, masks, tensor shapes, and a PyTorch implementation.
- [How to Generate Tokens Faster: A vLLM Performance Model](sources/vllm-performance-model.md) - Systems-modeling note that explains vLLM serving behavior through throughput, TTFT, queueing, and interference.
- [We're at AI's Halftime](sources/were-at-ais-halftime.md) - Essay arguing that AI progress is shifting from benchmark hillclimbing toward evaluation setups that better capture real utility.
- [Welcome to the Era of Experience](sources/welcome-to-the-era-of-experience.md) - Position paper arguing that future AI progress will come from long-horizon, grounded learning from experience.
- [The Geometry of Consolidation (NeurIPS 2026)](sources/geometry-of-consolidation-v6.md) - Paper proving the Consolidation-Interference Duality, with companion repository reproduction notes folded into the same source page.
- [Language Modeling Is Compression](sources/language-modeling-is-compression.md) - DeepMind paper showing LLMs as general-purpose compressors via the prediction-compression equivalence, with cross-modal compression results.
- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](sources/kv-cache-architecture-survey.md) - Undated survey of KVCache optimization from MHA through sparse and linear attention; its frontier architecture figures require primary-source verification.
- [向量数据库 (Vector Database)](sources/vector-database-overview.md) - Chinese introductory article on vector databases, ANN algorithms, similarity measurement, and database selection.
- [探秘Transformer系列之（1）：注意力机制](sources/cnblogs-transformer-series-01-attention-mechanism.md) - Chinese series opener deriving attention from Seq2Seq, CNN/RNN limits, alignment, long dependency, and QKV attention history.
- [探秘Transformer系列之（2）---总体架构](sources/cnblogs-transformer-series-02-overall-architecture.md) - Transformer architecture walkthrough covering tokenization-to-sampling flow, encoder/decoder modules, three attention types, and code construction.
- [探秘Transformer系列之（3）---数据处理](sources/cnblogs-transformer-series-03-data-processing.md) - Data-processing chapter on dataset quality, Multi30k, tokenizer/vocabulary loading, dataloaders, padding, and masks.
- [探秘Transformer系列之（4）--- 编码器 & 解码器](sources/cnblogs-transformer-series-04-encoder-decoder.md) - Encoder, decoder, cross-attention, tensor shapes, and decoder-only architecture explanation.
- [探秘Transformer系列之（5）--- 训练&推理](sources/cnblogs-transformer-series-05-training-and-inference.md) - Training versus inference guide covering teacher forcing, dropout, loss, labels, and autoregressive decode.
- [探秘Transformer系列之（6）--- token](sources/cnblogs-transformer-series-06-token.md) - Tokenization tutorial covering tokenizer stages, vocabularies, BPE, WordPiece, Unigram, SentencePiece, and multilingual trade-offs.
- [探秘Transformer系列之（7）--- embedding](sources/cnblogs-transformer-series-07-embedding.md) - Embedding chapter connecting token IDs, dense vectors, Transformer embedding layers, text embeddings, and weight tying.
- [探秘Transformer系列之（8）--- 位置编码](sources/cnblogs-transformer-series-08-positional-encoding.md) - Positional encoding chapter on order blindness, sinusoidal encodings, properties, and NoPE.
- [探秘Transformer系列之（9）--- 位置编码分类](sources/cnblogs-transformer-series-09-positional-encoding-taxonomy.md) - Taxonomy of absolute and relative positional encodings and where position information enters attention.
- [探秘Transformer系列之（10）--- 自注意力](sources/cnblogs-transformer-series-10-self-attention.md) - Self-attention deep dive on Q/K/V projections, scaled dot-product attention, tensor shapes, and optimization targets.
- [探秘Transformer系列之（11）--- 掩码](sources/cnblogs-transformer-series-11-masks.md) - Masking chapter distinguishing padding masks, causal sequence masks, dataflow, and advanced mask behavior.
- [探秘Transformer系列之（12）--- 多头自注意力](sources/cnblogs-transformer-series-12-multi-head-self-attention.md) - Multi-head self-attention guide covering head splitting, concatenation, output projection, and MQA/GQA motivations.
- [探秘Transformer系列之（13）--- FFN](sources/cnblogs-transformer-series-13-ffn.md) - FFN chapter on expand-activate-project structure, per-token nonlinear processing, knowledge use, and FFN evolution.
- [探秘Transformer系列之（14）--- 残差网络和归一化](sources/cnblogs-transformer-series-14-residuals-and-normalization.md) - Residual and normalization guide covering LayerNorm, BatchNorm, Pre-Norm/Post-Norm, RMSNorm, and DeepNorm.
- [探秘Transformer系列之（15）--- 采样和输出](sources/cnblogs-transformer-series-15-sampling-and-output.md) - Output and sampling chapter covering LM head, logits, temperature, Top-K, Top-P, sampling parameters, and weight tying.
- [探秘Transformer系列之（16）--- 资源占用](sources/cnblogs-transformer-series-16-resource-usage.md) - Resource-estimation chapter for Transformer parameters, memory, compute, training/inference state, and optimization directions.
- [探秘Transformer系列之（17）--- RoPE](sources/cnblogs-transformer-series-17-rope.md) - RoPE deep dive on Q/K rotation, relative-position dot products, properties, and implementation.
- [探秘Transformer系列之（18）--- FlashAttention](sources/cnblogs-transformer-series-18-flashattention.md) - FlashAttention V1 explanation covering IO-aware tiling, online softmax, exact attention, and memory traffic.
- [探秘Transformer系列之（19）----FlashAttention V2 及升级版本](sources/cnblogs-transformer-series-19-flashattention-v2-and-beyond.md) - FlashAttention V2, Flash-Decoding, Flash-Mask, and FlashAttention-3 kernel evolution overview.
- [探秘Transformer系列之（20）--- KV Cache](sources/cnblogs-transformer-series-20-kv-cache.md) - KV cache tutorial explaining prefill cache construction, decode cache reads/appends, complexity reduction, and memory cost.
- [探秘Transformer系列之（21）--- MoE](sources/cnblogs-transformer-series-21-moe.md) - Mixture-of-Experts guide covering routers, experts, sparse activation, load balancing, and expert parallelism.
- [探秘Transformer系列之（22）--- LoRA](sources/cnblogs-transformer-series-22-lora.md) - LoRA tutorial on low-rank adapters, frozen base weights, resource savings, implementation, and variants.
- [探秘Transformer系列之（23）--- 长度外推](sources/cnblogs-transformer-series-23-length-extrapolation.md) - Long-context extrapolation chapter on RoPE scaling, position interpolation, and trained-length mismatch.
- [探秘Transformer系列之（24）--- KV Cache优化](sources/cnblogs-transformer-series-24-kv-cache-optimization.md) - KV cache optimization survey across formula terms, MQA/GQA/MLA, quantization, compression, reuse, and system policy.
- [探秘Transformer系列之（25）--- KV Cache优化之处理长文本序列](sources/cnblogs-transformer-series-25-kv-cache-long-context.md) - Long-context KV cache optimization chapter on sparse retention, reuse, and retrieval-like cache schemes.
- [探秘Transformer系列之（26）--- KV Cache优化---分离or合并](sources/cnblogs-transformer-series-26-kv-cache-split-or-merge.md) - Serving architecture comparison of colocated chunked-prefill scheduling versus prefill/decode disaggregation.
- [探秘Transformer系列之（27）--- MQA & GQA](sources/cnblogs-transformer-series-27-mqa-and-gqa.md) - Attention-variant chapter explaining MHA, MQA, and GQA trade-offs for KV cache and decode bandwidth.
- [探秘Transformer系列之（28）--- DeepSeek MLA](sources/cnblogs-transformer-series-28-deepseek-mla.md) - DeepSeek MLA explanation covering latent KV compression, RoPE split handling, computation flow, and code conversion.
- [探秘Transformer系列之（29）--- DeepSeek MoE](sources/cnblogs-transformer-series-29-deepseek-moe.md) - DeepSeek MoE chapter on fine-grained experts, shared experts, routing difficulty, and expert-parallel serving implications.
- [探秘Transformer系列之（30）--- 投机解码](sources/cnblogs-transformer-series-30-speculative-decoding.md) - Speculative decoding guide covering draft/target verification, blockwise decoding, rejection sampling, and token-tree verification.
- [探秘Transformer系列之（31）--- Medusa](sources/cnblogs-transformer-series-31-medusa.md) - Medusa decoding guide covering multiple future-token heads, tree verification, training, and decoding.
- [探秘Transformer系列之（32）--- Lookahead Decoding](sources/cnblogs-transformer-series-32-lookahead-decoding.md) - Lookahead decoding guide covering Jacobi decoding, 2D windows, n-gram pools, verification, and llama.cpp implementation.
- [探秘Transformer系列之（33）--- DeepSeek MTP](sources/cnblogs-transformer-series-33-deepseek-mtp.md) - Multi-token prediction chapter covering EAGLE, MTP objectives, DeepSeek MTP structure, and verification use.
- [探秘Transformer系列之（34）--- 量化基础](sources/cnblogs-transformer-series-34-quantization-basics.md) - Quantization basics covering scale/zero-point, symmetric/asymmetric schemes, PTQ, QAT, calibration, and error.
- [探秘Transformer系列之（35）--- 大模型量化基础](sources/cnblogs-transformer-series-35-llm-quantization-basics.md) - LLM quantization challenges around activation outliers, super outliers, and Transformer-specific sensitivity.
- [探秘Transformer系列之（36）--- 大模型量化方案](sources/cnblogs-transformer-series-36-llm-quantization-methods.md) - LLM quantization methods covering 8-bit, 4-bit, GPTQ, AWQ, SmoothQuant, QLoRA, and lower-bit/KV quantization.

## Topics

- [CUDA Programming](topics/cuda-programming.md) - Durable overview of CUDA execution, synchronization, and performance-sensitive design.
- [AI-Native Learning](topics/ai-native-learning.md) - Interview-framed shift from memorization and exam drilling toward self-directed, first-principles, AI-assisted open-ended learning.
- [Disaggregated LLM Inference](topics/disaggregated-llm-inference.md) - Serving view that separates prefill and decode while tracking colocated chunked-prefill schedulers as a partial interference-mitigation alternative.
- [Experiential AI](topics/experiential-ai.md) - View of advanced agents as long-lived, grounded learners, plus the live dispute over human-derived priors, algorithms, evaluation, and reliability.
- [LLM Deployment and Capacity Planning](topics/llm-deployment-and-capacity-planning.md) - Operating view of model serving focused on memory planning, latency metrics, batching, KV cache, MoE, LoRA, quantization, and decoding acceleration.
- [Private Credit](topics/private-credit.md) - Non-bank lending market spanning direct lending, asset-based finance, and increasingly entangled funding channels.
- [Transformer Architecture and Attention](topics/transformer-architecture-and-attention.md) - Foundational model of tokenization, embeddings, masks, attention, RoPE, FFN, normalization, decoder-only generation, KV cache, MoE, and long-context behavior.
- [Embedding Memory Geometry](topics/embedding-memory-geometry.md) - Geometric study of semantic memory: effective dimension, consolidation limits, and centroid behavior on the paper's evaluated text corpora.
- [Compression and Language Models](topics/compression-and-language-models.md) - Prediction-compression equivalence, LLMs as general-purpose cross-modal compressors, and scaling-law insights from adjusted compression rates.
- [Vector Database and ANN Search](topics/vector-database-and-ann-search.md) - Vector databases for RAG and semantic search, covering ANN algorithms (K-Means, PQ, HNSW, LSH), similarity measures, and filtering strategies.

## Concepts

- [Attention Mechanism](concepts/attention-mechanism.md) - Q/K/V weighting operation behind self-attention, multi-head attention implementation, masking variants, online-softmax memory reductions, FlashAttention, and KV cache.
- [FlashAttention](concepts/flashattention.md) - Exact attention kernel family progressing from IO-aware SRAM tiling to better warp/sequence partitioning and Hopper FP8/asynchronous execution.
- [Autoregressive Generation](concepts/autoregressive-generation.md) - Next-token generation loop that creates prefill/decode phases, KV-cache reuse, TTFT/TPOT trade-offs, and chunked iteration-level scheduling needs.
- [Chunked Prefill Scheduling](concepts/chunked-prefill-scheduling.md) - Token-budgeted prompt processing technique that splits long prefills and mixes chunks with decode work to reduce generation stalls.
- [Token Sampling Strategies](concepts/token-sampling-strategies.md) - Greedy, temperature, Top-K, and Top-P policies for choosing the next token from logits during autoregressive generation.
- [Speculative Decoding](concepts/speculative-decoding.md) - Decode acceleration technique where candidate tokens are proposed and target-model verification plus rejection sampling preserves the output distribution.
- [Brain-Inspired AI](concepts/brain-inspired-ai.md) - Neuroscience-informed view that future AI may need richer neural complexity, long-range feedback, parallel perception, and embodied action loops.
- [Context Caching in LLM Serving](concepts/context-caching-in-llm-serving.md) - Reuse of prefix KV state across requests to reduce repeated prefill work.
- [CUDA Thread Hierarchy](concepts/cuda-thread-hierarchy.md) - The `Grid -> Block -> Thread` structure that defines CUDA work partitioning.
- [Grounded Rewards](concepts/grounded-rewards.md) - Environmental feedback signals used to optimize agent behavior beyond human prejudgement.
- [GPU Memory Hierarchy](concepts/gpu-memory-hierarchy.md) - The trade-offs among registers, shared memory, local memory, and global memory.
- [Integer-Only Quantization](concepts/integer-only-quantization.md) - Low-bit deployment approach using scale/zero-point mappings, outlier-aware LLM treatment, PTQ/QAT, and hardware-efficient integer paths.
- [Iteration-Level Scheduling](concepts/iteration-level-scheduling.md) - Serving policy that re-forms batches after each generation step and needs token-budget rules to prevent full-prefill stalls.
- [KV Cache in LLM Serving](concepts/kv-cache-in-llm-serving.md) - Why attention cache dominates variable inference memory and how MQA/GQA/MLA, quantization, sparse retention, reuse, and long-context planning change it.
- [Model Bandwidth Utilization](concepts/model-bandwidth-utilization.md) - A normalized measure of inference memory-bandwidth efficiency and decode-side compute slack exploitable by bounded prefill work.
- [PagedAttention](concepts/pagedattention.md) - Block-based KV-cache layout that trades contiguous allocation for much better utilization and sharing.
- [Parallelism in LLM Serving](concepts/parallelism-in-llm-serving.md) - Tensor/expert parallelism distinctions, including attention-head splits, FFN partitioning, MoE token dispatch, and phase-aware serving.
- [Prefill-Decode Disaggregation](concepts/prefill-decode-disaggregation.md) - Separation of parallel prompt processing and sequential KV-cache-heavy token generation into different serving pools, contrasted with colocated chunked-prefill schedulers.
- [Rated Note Feeders](concepts/rated-note-feeders.md) - Structured wrappers that make private-credit exposure easier for regulated investors to hold.
- [Streams of Experience](concepts/streams-of-experience.md) - Long-lived action-observation trajectories that support adaptation and long-horizon optimization.
- [Unitranche Loans](concepts/unitranche-loans.md) - Single-loan structures that merge senior and junior debt to trade clarity for execution speed.
- [Utility Problem](concepts/utility-problem.md) - The gap between benchmark capability and durable real-world usefulness when evaluation setups miss how work actually happens.
- [Effective Dimension](concepts/effective-dimension.md) - Participation ratio measuring how many independent directions a cluster's covariance occupies and governing the Consolidation-Interference Duality bound.
- [Prediction-Compression Equivalence](concepts/prediction-compression-equivalence.md) - Information-theoretic bridge between probabilistic prediction, cross-entropy, and lossless compression.
- [Positional Encoding](concepts/positional-encoding.md) - Order signal for Transformers, covering absolute/relative encodings, RoPE Q/K rotation, ALiBi score bias, and long-context extrapolation.
- [Multi-head Latent Attention (MLA)](concepts/multi-head-latent-attention-mla.md) - DeepSeek attention variant that stores low-rank latent KV state; an undated survey reports approximately 96% dimensional reduction at V3 scale.
- [Tokenization and Embeddings](concepts/tokenization-and-embeddings.md) - Text-to-token and token-to-vector input layer, including tokenizer stages, subword tokenization, embedding tables, vocabulary memory, and weight tying.
- [Transformer Feed-Forward Network](concepts/transformer-feed-forward-network.md) - Per-token nonlinear Transformer sublayer covering standard FFN, SwiGLU, dense parameter share, tensor-parallel splits, and MoE expertization.
- [Transformer Normalization and Residuals](concepts/transformer-normalization-and-residuals.md) - Stability machinery for deep Transformer stacks: residual identity paths, LayerNorm/RMSNorm, Pre-Norm, and fused residual-norm kernels.
- [Product Quantization](concepts/product-quantization.md) - Vector compression by sub-vector quantization with learned codebooks, commonly used in large-scale ANN search.
- [Hierarchical Navigable Small Worlds (HNSW)](concepts/hierarchical-navigable-small-worlds-hnsw.md) - Multi-layer graph-based ANN algorithm with top-down search from long-jump to dense-granularity layers.
- [Mixture of Experts](concepts/mixture-of-experts.md) - Sparse expert FFN routing that expands total model capacity while introducing router, load-balancing, and expert-parallel serving constraints.
- [Low-Rank Adaptation (LoRA)](concepts/low-rank-adaptation-lora.md) - Parameter-efficient fine-tuning by training low-rank adapter updates on top of frozen base-model weights.
- [Long Context Extrapolation](concepts/long-context-extrapolation.md) - Making Transformers remain useful beyond trained context length through position scaling plus KV/memory strategies.
- [Parallel Decoding Variants](concepts/parallel-decoding-variants.md) - Medusa, Lookahead, MTP, and related methods that propose or verify multiple future tokens to reduce serial decode steps.
- [LLM Quantization](concepts/llm-quantization.md) - LLM-specific low-precision deployment covering outlier-aware weights, activations, KV cache, GPTQ/AWQ/SmoothQuant, and QLoRA.

## Synthesis

- [AI Halftime vs Bitter Lesson and Era of Experience](synthesis/ai-halftime-vs-bitter-lesson-and-era-of-experience.md) - Comparative analysis of the substantive but staged conflict over language priors, grounded experience, algorithms, and reliability.
