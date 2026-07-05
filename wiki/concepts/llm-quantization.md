# LLM Quantization

LLM quantization reduces model and runtime numeric precision to lower memory use, bandwidth pressure, and sometimes latency, while trying to preserve generation quality.

## Why It Matters

- Quantization can target weights, activations, KV cache, or combinations of them; each target has different quality and kernel constraints.
- LLM activations often contain outlier channels or tokens, so naive low-bit quantization can waste range on extremes and damage ordinary values.
- PTQ methods such as GPTQ or AWQ use calibration data and error-aware approximations to quantize trained models without full retraining.
- SmoothQuant-like methods shift difficulty between activations and weights to make activation quantization easier.
- 4-bit methods reduce weight memory aggressively, while 8-bit methods are usually easier to deploy with lower quality risk.
- Quantization only improves serving if the hardware and inference stack execute the lower-precision path efficiently.
- FP8 attention needs kernel-specific accuracy controls, not only smaller tensors: FlashAttention-3 uses block quantization and incoherent processing to reduce outlier-driven FP8 error while targeting Hopper Tensor Cores.

## Related Pages

- [Integer-Only Quantization](integer-only-quantization.md)
- [KV Cache in LLM Serving](kv-cache-in-llm-serving.md)
- [Low-Rank Adaptation (LoRA)](low-rank-adaptation-lora.md)
- [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- [FlashAttention](flashattention.md)

## Sources

- [探秘Transformer系列之（34）--- 量化基础](../sources/cnblogs-transformer-series-34-quantization-basics.md)
- [探秘Transformer系列之（35）--- 大模型量化基础](../sources/cnblogs-transformer-series-35-llm-quantization-basics.md)
- [探秘Transformer系列之（36）--- 大模型量化方案](../sources/cnblogs-transformer-series-36-llm-quantization-methods.md)
- [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](../sources/quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference.md)
- [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](../sources/flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-precision.md)
