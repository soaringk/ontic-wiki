# Transformer Feed-Forward Network

Transformer FFN is the per-token nonlinear sublayer that follows attention inside each block.

## Why It Matters

- Attention mixes information across tokens; FFN independently transforms each token's hidden vector after that mixing.
- Standard FFN uses an expand-activate-project pattern, usually `d_model -> 4*d_model -> d_model`.
- Modern LLMs commonly use SwiGLU, which adds a gate projection and usually lowers the intermediate dimension to about `8/3*d_model` to keep parameter count close to the standard FFN.
- FFN often holds about two thirds of dense Decoder Block parameters, so it dominates weight memory, quantization impact, and tensor-parallel communication design.
- Megatron-style tensor parallelism usually column-splits `W_up`/`W_gate` and row-splits `W_down`, leaving one final AllReduce for the FFN output.
- MoE architectures usually expertize the FFN, routing each token to a small subset of expert FFNs to increase total capacity without activating every parameter.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- [Parallelism in LLM Serving](parallelism-in-llm-serving.md)

## Sources

- [3.4 Transformer前馈网络FFN深入理解](../sources/transformer-ffn-deep-dive.md)
- [3.7 Transformer Decoder Block完整解析](../sources/transformer-decoder-block-deep-dive.md)
- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
