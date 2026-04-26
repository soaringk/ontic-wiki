# Integer-Only Quantization

Integer-only quantization represents weights and activations with low-bit integers plus scale and zero-point parameters so inference can run mostly or entirely with integer arithmetic.

## Why It Matters

- It can reduce model size, memory traffic, and latency on hardware with efficient integer units.
- Exact zero representation matters for padding and fused operator correctness.
- Good deployment accuracy usually requires quantization-aware training rather than naive post-training conversion.
- Higher-precision accumulators and biases are often still necessary.

## Related Pages

- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)

## Sources

- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](../sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md)
