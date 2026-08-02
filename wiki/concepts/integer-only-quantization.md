# Integer-Only Quantization

Integer-only quantization represents weights and activations with low-bit integers plus scale and zero-point parameters so inference can run mostly or entirely with integer arithmetic.

## Why It Matters

- It can reduce model size, memory traffic, and latency on hardware with efficient integer units.
- Exact zero representation matters for padding and fused operator correctness.
- Some already-efficient models may require quantization-aware training when naive post-training conversion causes unacceptable accuracy loss.
- Higher-precision accumulators and biases are often still necessary.
- Integer-only execution depends on affine scale/zero-point mappings, fixed-point multipliers, higher-precision accumulation, and kernels that preserve those arithmetic conventions.
- LLM-specific outlier handling, GPTQ/AWQ/SmoothQuant, KV-cache formats, and serving validation are tracked on [LLM Quantization](llm-quantization.md).

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [LLM Quantization](llm-quantization.md)

## Sources

- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](../sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md)
- [探秘Transformer系列之（34）--- 量化基础](../sources/cnblogs-transformer-series-34-quantization-basics.md)
