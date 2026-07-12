# Transformer Architecture and Attention

Transformer architecture models sequences by repeatedly letting each token update its representation using attention over other tokens. In the current wiki, this topic matters mainly because modern LLM serving papers assume familiarity with decoder-only autoregression, attention state reuse, and the difference between processing a full prompt in parallel and generating later tokens one by one.

## Core Ideas

- Tokenization converts text into a model vocabulary that the network can process as discrete tokens.
- Embeddings map tokens into vectors that the network can transform layer by layer.
- Data handling, vocabulary construction, padding, and mask construction are part of the model contract because they determine token IDs, tensor shapes, and valid attention boundaries.
- Self-attention lets each token weight other tokens differently depending on context.
- Scaled dot-product attention scores token pairs with `QK^T / sqrt(d_k)`, normalizes the scores with softmax, and uses the result to aggregate V.
- Multi-head attention runs several attention projections in parallel, giving the model multiple relation subspaces and giving infrastructure a natural tensor-parallel split point.
- Decoder-side causal masking enforces autoregressive generation by blocking access to future tokens.
- Padding masks, causal masks, and cross-attention masks encode different information boundaries and should not be collapsed into one generic "attention mask" mental model.
- Encoder-decoder Transformers and decoder-only LLMs share attention primitives but differ in how generation is structured.
- Modern decoder-only LLMs simplify the path to `Embedding -> repeated decoder blocks -> final norm -> LM head`, which makes KV-cache behavior and inference scheduling easier to reason about.
- RoPE, LayerNorm/RMSNorm placement, residual connections, FFN shape, and tokenization/embedding choices are part of the serving-relevant architecture because they affect kernel fusion, stability, parameter count, vocabulary memory, and long-context behavior.
- FFN is the per-token nonlinear path after attention; in dense decoder blocks it commonly owns about two thirds of parameters, while SwiGLU changes the gate/up/down shape without necessarily increasing total FFN parameters.
- Pre-Norm plus residual connections keep the gradient path stable in deep decoder stacks; RMSNorm is now common because it preserves scale control with less reduction work than full LayerNorm.
- Position encoding is the answer to self-attention's order blindness; RoPE is dominant because it injects relative position through Q/K rotation and works well with fused attention kernels.
- Tokenization and embeddings define the model's actual discrete input space; vocabulary size changes both multilingual efficiency and embedding/LM-head memory.
- Autoregressive generation turns architecture into a serving loop: prompt prefill builds KV state, decode appends one token at a time, and sampling policy chooses from the next-token distribution.
- Sampling policies such as greedy decoding, temperature, Top-K, and Top-P operate after the LM head over logits; they change output behavior without changing the attention architecture.
- KV cache exists because later decoding steps reuse previously computed attention keys and values instead of recomputing the full prefix each time.
- Attention variants such as MQA, GQA, and MLA preserve many query pathways while reducing or compressing the key/value state that inference must store and read.
- Sparse attention can reduce retained history through sliding windows or learned selection. Compression ratios for frontier variants such as CSA+HCA are architecture-specific and currently represented here only by an undated survey.
- Linear or recurrent attention variants replace growing per-token KV state with fixed-size state at those layers. Hybrid architectures interleave them with full-attention layers, retaining some sequence-length-dependent cache and model-specific quality trade-offs.
- Cross-Layer Attention (CLA) reduces KVCache by having adjacent layers share K/V state instead of computing and storing them independently.
- MoE changes the FFN path by routing each token to a small subset of experts, expanding total capacity while adding routing, load-balancing, and expert-parallel communication constraints.
- Long-context extrapolation is a position-generalization problem as well as a memory problem: RoPE scaling can extend usable context only if quality survives the new position distribution.

## Why It Matters For Serving

- Prefill is the phase that processes the prompt and builds the initial KV cache.
- Decode is slower and more sequential because each new token depends on all prior context.
- Prefill attention usually looks like large matrix multiplication, while decode attention often becomes memory-bound because it reads weights and KV cache for one new token at a time.
- Transformer code structure maps directly to infrastructure work: attention Q/K/V and output projections are GEMM targets, softmax is a fusion/IO target, FFN matrices dominate parameter count, and LayerNorm/RMSNorm plus residual paths are common kernel-fusion boundaries.
- Decoder Block arithmetic can be planned component by component: embeddings and LM head scale with vocabulary, attention scales with Q/K/V/O projections and KV-head count, FFN scales with intermediate width, and KV Cache scales with layer count, KV heads, head dimension, sequence length, batch, dtype, and tensor parallelism.
- FlashAttention attacks the attention module's memory traffic and intermediate materialization costs by tiling attention and using online softmax to avoid writing the full attention matrix to high-bandwidth memory.
- FlashAttention-2 and FlashAttention-3 show that exact attention kernel performance depends on more than asymptotic complexity: sequence-block parallelism, warp work partitioning, asynchronous data movement, GEMM-softmax overlap, and low-precision layout constraints all affect usable long-context throughput.
- Exact attention does not have to materialize an `n x n` attention matrix: online softmax accumulation and chunking can preserve dense attention semantics while reducing activation memory, although time remains quadratic.
- GQA and MQA reduce KV-cache footprint by using fewer key/value heads than query heads.
- Many serving optimizations are really attempts to manage the memory, parallelism, and scheduling consequences of causal attention.

## Related Concepts

- [Attention Mechanism](../concepts/attention-mechanism.md)
- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- [Transformer Feed-Forward Network](../concepts/transformer-feed-forward-network.md)
- [Positional Encoding](../concepts/positional-encoding.md)
- [Transformer Normalization and Residuals](../concepts/transformer-normalization-and-residuals.md)
- [Autoregressive Generation](../concepts/autoregressive-generation.md)
- [Token Sampling Strategies](../concepts/token-sampling-strategies.md)
- [Tokenization and Embeddings](../concepts/tokenization-and-embeddings.md)
- [Mixture of Experts](../concepts/mixture-of-experts.md)
- [Long Context Extrapolation](../concepts/long-context-extrapolation.md)
- [FlashAttention](../concepts/flashattention.md)

## Sources

- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
- [Transformer Overview and Code Implementation](../sources/transformer-overview-and-code-implementation.md)
- [Self-Attention Mechanism Deep Dive](../sources/self-attention-mechanism-deep-dive.md)
- [3.4 Transformer前馈网络FFN深入理解](../sources/transformer-ffn-deep-dive.md)
- [3.5 Transformer位置编码深入理解](../sources/transformer-positional-encoding-deep-dive.md)
- [3.6 LayerNorm与残差连接深入理解](../sources/layernorm-and-residual-connections-deep-dive.md)
- [3.7 Transformer Decoder Block完整解析](../sources/transformer-decoder-block-deep-dive.md)
- [3.8 从Transformer到LLM自回归生成深入理解](../sources/transformer-to-llm-autoregressive-generation.md)
- [3.9 Tokenization与词嵌入](../sources/tokenization-and-word-embedding.md)
- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](../sources/kv-cache-architecture-survey.md)
- [Self-attention Does Not Need O(n^2) Memory](../sources/self-attention-does-not-need-o-n2-memory.md)
- [Accelerating Large Language Model Decoding with Speculative Sampling](../sources/accelerating-large-language-model-decoding-with-speculative-sampling.md)
- [探秘Transformer系列之（1）：注意力机制](../sources/cnblogs-transformer-series-01-attention-mechanism.md)
- [探秘Transformer系列之（2）---总体架构](../sources/cnblogs-transformer-series-02-overall-architecture.md)
- [探秘Transformer系列之（3）---数据处理](../sources/cnblogs-transformer-series-03-data-processing.md)
- [探秘Transformer系列之（4）--- 编码器 & 解码器](../sources/cnblogs-transformer-series-04-encoder-decoder.md)
- [探秘Transformer系列之（6）--- token](../sources/cnblogs-transformer-series-06-token.md)
- [探秘Transformer系列之（8）--- 位置编码](../sources/cnblogs-transformer-series-08-positional-encoding.md)
- [探秘Transformer系列之（10）--- 自注意力](../sources/cnblogs-transformer-series-10-self-attention.md)
- [探秘Transformer系列之（11）--- 掩码](../sources/cnblogs-transformer-series-11-masks.md)
- [探秘Transformer系列之（13）--- FFN](../sources/cnblogs-transformer-series-13-ffn.md)
- [探秘Transformer系列之（14）--- 残差网络和归一化](../sources/cnblogs-transformer-series-14-residuals-and-normalization.md)
- [探秘Transformer系列之（15）--- 采样和输出](../sources/cnblogs-transformer-series-15-sampling-and-output.md)
- [探秘Transformer系列之（17）--- RoPE](../sources/cnblogs-transformer-series-17-rope.md)
- [探秘Transformer系列之（18）--- FlashAttention](../sources/cnblogs-transformer-series-18-flashattention.md)
- [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](../sources/flashattention-fast-and-memory-efficient-exact-attention-with-io-awareness.md)
- [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](../sources/flashattention-2-faster-attention-with-better-parallelism-and-work-partitioning.md)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](../sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md)
- [探秘Transformer系列之（21）--- MoE](../sources/cnblogs-transformer-series-21-moe.md)
- [探秘Transformer系列之（23）--- 长度外推](../sources/cnblogs-transformer-series-23-length-extrapolation.md)
