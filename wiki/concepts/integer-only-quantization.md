# Integer-Only Quantization

Integer-only quantization represents weights and activations with low-bit integers plus scale and zero-point parameters so inference can run mostly or entirely with integer arithmetic.

## Why It Matters

- It can reduce model size, memory traffic, and latency on hardware with efficient integer units.
- Exact zero representation matters for padding and fused operator correctness.
- Good deployment accuracy usually requires quantization-aware training rather than naive post-training conversion.
- Higher-precision accumulators and biases are often still necessary.
- LLM-specific quantization must handle activation outliers, per-channel variation, KV-cache precision, and hardware/kernel support; reducing checkpoint size alone does not guarantee lower serving latency.
- PTQ methods such as GPTQ/AWQ and smoothing methods such as SmoothQuant are practical LLM quantization paths, while QAT remains useful when deployment hardware and quality targets justify retraining cost.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [LLM Quantization](llm-quantization.md)

## Sources

- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](../sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md)
- [探秘Transformer系列之（34）--- 量化基础](../sources/cnblogs-transformer-series-34-quantization-basics.md)
- [探秘Transformer系列之（35）--- 大模型量化基础](../sources/cnblogs-transformer-series-35-llm-quantization-basics.md)
- [探秘Transformer系列之（36）--- 大模型量化方案](../sources/cnblogs-transformer-series-36-llm-quantization-methods.md)
