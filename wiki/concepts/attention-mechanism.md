# Attention Mechanism

Attention is the operation that lets each token weight and aggregate information from other relevant tokens in its context.

## Why It Matters

- It gives Transformer models flexible long-range dependency handling.
- Decoder-only generation depends on causal attention that only sees past tokens.
- The need to reuse prior keys and values is what creates KV cache during inference.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)

## Sources

- [Transformer and Attention, Explained Plainly](../sources/transformer-and-attention-a-layman-guide.md)
