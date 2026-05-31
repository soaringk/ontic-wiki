---
kind: source
title: "从 305 GB 到 7.4 GB：大模型 KVCache 架构演进全景"
slug: kv-cache-architecture-survey
source_ids:
  - raw-kv-cache-architecture-survey
status: active
raw_path: raw/kv-cache-architecture-survey.md
source_type: markdown
parser: direct
published: unknown
created: 2026-05-26
updated: 2026-05-26
---

# Summary

A comprehensive Chinese survey article tracing the evolution of KVCache optimization across LLM architectures, from MHA through MQA, GQA, MLA, sparse attention, linear attention, and Cross-Layer Attention (CLA). It quantifies how the per-token KV footprint dropped from 320 KB (Qwen2.5-72B GQA) to 7.7 KB (DeepSeek V4 CSA+HCA) at 1M context — a ~41× reduction — and explains the engineering trade-offs behind each approach.

# Key Claims

- **Three core KV compression axes.** (1) Reduce KV head count (MHA → MQA → GQA). (2) Compress KV representation (MLA: 96% dimension reduction). (3) Reduce tokens needing KV (sparse attention, sliding windows).
- **MLA (Multi-head Latent Attention).** DeepSeek V2/V3 compresses K and V jointly into a low-rank latent vector; at DeepSeek V3 scale, single-layer KVCache drops from 14,336 to 576 dimensions (~96% reduction) with quality intact or improved.
- **CSA+HCA (DeepSeek V4).** Hybrid layer-level compression: 30 layers of CSA (4:1 overlap-compressed + top-k sparse) + 31 layers of HCA (128:1 block-compressed with dense attention). At 1M context, V4 KVCache ≈ 7.4 GB vs V3's 65 GB — about 10% of V3.
- **Linear attention (Mamba → Gated DeltaNet → hybrid).** Replaces growing KVCache with fixed-size hidden state: Mamba/SSM uses O(1) state vectors; Gated DeltaNet uses d×d associative memory matrix with dual gating (α for global forgetting, β for precise delta updates); hybrid architectures (Qwen3.5, Jamba) interleave linear attention layers with full-attention layers for a ~75% KVCache reduction.
- **Quantization.** FP8 halves KV memory relative to BF16 with negligible quality loss; NVFP4 halves again. Vector compression (TurboQuant) reaches ~3.5 bits per dimension.
- **Cross-Layer Attention (CLA).** Adjacent layers share K/V state, halving KVCache — orthogonal to GQA/MLA.
- **MoE amplifies KVCache importance.** MoE reduces FFN activation memory, making KVCache a larger fraction of total inference memory (60–80%).

# Why It Matters

This survey provides a structured roadmap of the KVCache optimization landscape, from production-ready techniques (GQA, FP8 quantization) through frontier architectures (MLA, CSA+HCA, Gated DeltaNet hybrids). It gives concrete, comparable memory numbers across architectures and connects each optimization to its engineering cost.

# Connections

- Topic: [Transformer Architecture and Attention](../topics/transformer-architecture-and-attention.md)
- Concept: [KV Cache in LLM Serving](../concepts/kv-cache-in-llm-serving.md)
- Concept: [Attention Mechanism](../concepts/attention-mechanism.md)
- Concept: [Multi-head Latent Attention (MLA)](../concepts/multi-head-latent-attention-mla.md)

# Open Questions

- Linear attention hybrids (Qwen3.5 pattern) vs. sparse attention (DeepSeek V4 pattern) represent two competing future directions; no consensus on which wins at scale.
- Cross-Layer Attention (CLA) remains mostly academic; its interaction with MLA and sparse attention at production scale is underexplored.
