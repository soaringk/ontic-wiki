# Transformer Normalization and Residuals

Normalization and residual connections are the stability scaffolding that lets deep Transformer stacks train and run reliably.

## Why It Matters

- Residual connections add an identity path around attention and FFN sublayers, letting gradients propagate through deep networks without relying only on chained nonlinear transformations.
- LayerNorm normalizes each token across its feature dimension, avoiding BatchNorm's dependence on batch statistics and making training and inference behavior consistent.
- RMSNorm removes mean-centering and keeps RMS scaling, reducing memory-bound normalization work while preserving the scale-control role important in LLMs.
- Pre-Norm keeps the residual path clean by applying normalization before each sublayer; this is a major reason deep decoder-only LLMs train more stably.
- Post-Norm can work but usually needs more careful optimization because LayerNorm sits on the residual path.
- Residual Add + LayerNorm/RMSNorm fusion is an important kernel boundary because it avoids writing and rereading intermediate residual states from HBM.

## Related Pages

- [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)

## Sources

- [3.6 LayerNorm与残差连接深入理解](../sources/layernorm-and-residual-connections-deep-dive.md)
- [3.7 Transformer Decoder Block完整解析](../sources/transformer-decoder-block-deep-dive.md)
- [Transformer Architecture Quick Start](../sources/transformer-architecture-quick-start.md)
