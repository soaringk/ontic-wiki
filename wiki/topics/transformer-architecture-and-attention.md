# Transformer Architecture and Attention

Transformer architecture models sequences by repeatedly letting each token update its representation using attention over other tokens. In the current wiki, this topic matters mainly because modern LLM serving papers assume familiarity with decoder-only autoregression, attention state reuse, and the difference between processing a full prompt in parallel and generating later tokens one by one.

## Core Ideas

- Tokenization converts text into a model vocabulary that the network can process as discrete tokens.
- Embeddings map tokens into vectors that the network can transform layer by layer.
- Self-attention lets each token weight other tokens differently depending on context.
- Scaled dot-product attention scores token pairs with `QK^T / sqrt(d_k)`, normalizes the scores with softmax, and uses the result to aggregate V.
- Multi-head attention runs several attention projections in parallel, giving the model multiple relation subspaces and giving infrastructure a natural tensor-parallel split point.
- Decoder-side causal masking enforces autoregressive generation by blocking access to future tokens.
- Padding masks, causal masks, and cross-attention masks encode different information boundaries and should not be collapsed into one generic "attention mask" mental model.
- Encoder-decoder Transformers and decoder-only LLMs share attention primitives but differ in how generation is structured.
- Modern decoder-only LLMs simplify the path to `Embedding -> repeated decoder blocks -> final norm -> LM head`, which makes KV-cache behavior and inference scheduling easier to reason about.
- RoPE, LayerNorm placement, residual connections, and FFN shape are part of the serving-relevant architecture because they affect kernel fusion, stability, parameter count, and long-context behavior.
- KV cache exists because later decoding steps reuse previously computed attention keys and values instead of recomputing the full prefix each time.
- Attention variants such as MQA, GQA, and MLA preserve many query pathways while reducing or compressing the key/value state that inference must store and read.
- Sparse attention (NSA, DSA, CSA+HCA) reduces the number of tokens whose KV must be retained by selectively keeping only the most relevant history — from simple sliding windows (SWA) through learned sparse selection to hybrid compression (CSA 4:1, HCA 128:1).
- Linear attention (Mamba/SSM, Gated DeltaNet) replaces the growing KV cache with a fixed-size hidden state, breaking the O(n) memory-sequences-length link at the cost of expressiveness. Hybrid architectures (Qwen3.5, Jamba) interleave linear attention layers with full-attention layers.
- Cross-Layer Attention (CLA) reduces KVCache by having adjacent layers share K/V state instead of computing and storing them independently.

## Why It Matters For Serving

- Prefill is the phase that processes the prompt and builds the initial KV cache.
- Decode is slower and more sequential because each new token depends on all prior context.
- Prefill attention usually looks like large matrix multiplication, while decode attention often becomes memory-bound because it reads weights and KV cache for one new token at a time.
- Transformer code structure maps directly to infrastructure work: attention Q/K/V and output projections are GEMM targets, softmax is a fusion/IO target, FFN matrices dominate parameter count, and LayerNorm/RMSNorm plus residual paths are common kernel-fusion boundaries.
- FlashAttention attacks the attention module's memory traffic and intermediate materialization costs by tiling attention and using online softmax to avoid writing the full attention matrix to high-bandwidth memory.
- GQA and MQA reduce KV-cache footprint by using fewer key/value heads than query heads.
- Many serving optimizations are really attempts to manage the memory, parallelism, and scheduling consequences of causal attention.

## Related Concepts

- [Attention Mechanism](../concepts/attention-mechanism.md)
- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

## Sources

- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
- [Transformer Overview and Code Implementation](../sources/transformer-overview-and-code-implementation.md)
- [Self-Attention Mechanism Deep Dive](../sources/self-attention-mechanism-deep-dive.md)
- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](../sources/kv-cache-architecture-survey.md)
