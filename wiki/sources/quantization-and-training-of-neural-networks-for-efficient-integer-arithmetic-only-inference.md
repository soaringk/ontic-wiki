---
kind: source
title: Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference
slug: quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference
source_ids:
  - raw-quantization-and-training-of-neural-networks-for-efficient-integer-arithmetic-only-inference
status: active
raw_path: raw/Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference.pdf
source_type: pdf
published: unknown
created: 2026-04-25
updated: 2026-04-25
---

# Summary

This paper presents a practical 8-bit quantization scheme that preserves exact zero representation, supports integer-only inference, and pairs naturally with training-time fake quantization. Its core claim is that efficient deployment requires a co-design of quantized arithmetic, operator fusion, and quantization-aware training rather than post-hoc compression alone.

# Key Claims

- A useful quantization scheme should map integers to reals with an affine transform using scale and zero-point.
- Integer-only inference is viable when the non-integer multiplier is precomputed and implemented through fixed-point arithmetic plus shifts.
- Biases need higher precision than weights and activations to avoid systematic accuracy loss.
- Post-training quantization often fails on already-efficient small models; training must simulate quantization effects directly.
- Real hardware wins come from latency-vs-accuracy improvements, not just smaller stored weights.

# Why It Matters

This source grounds quantization in systems reality. It explains why low-bit deployment is not only about model size, but also about exact arithmetic conventions, fused kernels, and training procedures that preserve usable accuracy.

# Connections

- Topic: [LLM Deployment and Capacity Planning](../topics/llm-deployment-and-capacity-planning.md)
- Concept: [Integer-Only Quantization](../concepts/integer-only-quantization.md)

# Open Questions

- The paper focuses on mobile CNN deployment, so applying its exact arithmetic choices to current transformer inference requires care.
- It does not address the newer serving trade-off between weight quantization, KV-cache quantization, and end-user quality in large autoregressive models.
