# Attention Mechanism

Attention is the operation that lets each token weight and aggregate information from other relevant tokens in its context.

## Why It Matters

- It gives Transformer models flexible long-range dependency handling.
- Scaled dot-product attention projects hidden states into Q, K, and V, scores token pairs with `QK^T / sqrt(d_k)`, normalizes scores with softmax, and uses the result to weight V.
- The `sqrt(d_k)` scaling term keeps attention-score variance from growing with head dimension, reducing the risk that softmax saturates into near one-hot weights with weak gradients.
- Multi-head attention repeats that operation across separate heads, then merges the head outputs back into the model dimension.
- Multi-head attention has a concrete implementation shape: project to Q/K/V, split heads, run scaled dot-product attention independently per head, concatenate, then apply the output projection.
- Decoder-only generation depends on causal attention that only sees past tokens.
- Encoder self-attention, masked decoder self-attention, and cross-attention share the same scoring formula but differ in Q/K/V source and masking behavior.
- Infrastructure optimizations often target this exact computation: FlashAttention reduces attention memory traffic through tiling and online softmax, tensor parallelism can split heads, and GQA/MQA reduce key/value head count.
- MLA (Multi-head Latent Attention) compresses K and V jointly into a low-rank latent vector, caching the compressed representation and reconstructing on-the-fly — ~96% KV storage reduction at DeepSeek V3 scale.
- Sparse attention (NSA, DSA, CSA+HCA) reduces attention computation by selecting only the most relevant KV tokens, using learned or heuristic sparsity to skip computation on unimportant history.
- Linear attention (Mamba/SSM, Gated DeltaNet) replaces the QKV projection + softmax pattern with a fixed-size recurrent state, eliminating the need for KV cache entirely at the cost of reduced expressiveness.
- The need to reuse prior keys and values is what creates KV cache during inference.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)

## Sources

- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
- [Transformer Overview and Code Implementation](../sources/transformer-overview-and-code-implementation.md)
- [Self-Attention Mechanism Deep Dive](../sources/self-attention-mechanism-deep-dive.md)
- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
- [从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景](../sources/kv-cache-architecture-survey.md)
