# Transformer Architecture and Attention

Transformer architecture models sequences by repeatedly letting each token update its representation using attention over other tokens. In the current wiki, this topic matters mainly because modern LLM serving papers assume familiarity with decoder-only autoregression, attention state reuse, and the difference between processing a full prompt in parallel and generating later tokens one by one.

## Core Ideas

- Tokenization converts text into a model vocabulary that the network can process as discrete tokens.
- Embeddings map tokens into vectors that the network can transform layer by layer.
- Self-attention lets each token weight other tokens differently depending on context.
- Decoder-side causal masking enforces autoregressive generation by blocking access to future tokens.
- Encoder-decoder Transformers and decoder-only LLMs share attention primitives but differ in how generation is structured.
- KV cache exists because later decoding steps reuse previously computed attention keys and values instead of recomputing the full prefix each time.

## Why It Matters For Serving

- Prefill is the phase that processes the prompt and builds the initial KV cache.
- Decode is slower and more sequential because each new token depends on all prior context.
- Many serving optimizations are really attempts to manage the memory and scheduling consequences of causal attention.

## Related Concepts

- [Attention Mechanism](../concepts/attention-mechanism.md)
- [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)

## Sources

- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention](../sources/efficient-memory-management-for-large-language-model-serving-with-pagedattention.md)
