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

An undated Chinese survey article tracing KVCache optimization across LLM architectures, from MHA through MQA, GQA, MLA, sparse attention, linear attention, and Cross-Layer Attention (CLA). It reports a modeled per-token KV-footprint reduction from 320 KB (Qwen2.5-72B GQA) to 7.7 KB for a described DeepSeek V4 CSA+HCA design at 1M context, but the frontier architecture names and figures require verification against primary sources.

# Key Claims

- **Three core KV compression axes.** (1) Reduce KV head count (MHA → MQA → GQA). (2) Compress KV representation (MLA: 96% dimension reduction). (3) Reduce tokens needing KV (sparse attention, sliding windows).
- **MLA (Multi-head Latent Attention).** The survey reports that DeepSeek V2/V3 compress K and V jointly into a low-rank latent vector; at DeepSeek V3 scale, its dimensional comparison drops from 14,336 to 576 (~96%), with quality effects requiring model-specific evidence.
- **CSA+HCA (described as DeepSeek V4).** The survey describes 30 layers of CSA (4:1 overlap-compressed + top-k sparse) plus 31 layers of HCA (128:1 block-compressed with dense attention), and estimates about 7.4 GB at 1M context versus 65 GB for V3. Treat the architecture status and figures as survey claims pending primary-source verification.
- **Linear attention (Mamba → Gated DeltaNet → hybrid).** Replaces growing KVCache with fixed-size hidden state: Mamba/SSM uses O(1) state vectors; Gated DeltaNet uses a d×d associative memory matrix with dual gating; the survey attributes roughly 75% KVCache reduction to particular hybrid layer mixes.
- **Quantization.** FP8 halves element storage relative to BF16 and 4-bit formats halve it again; realized memory savings and quality effects depend on implementation and model. The survey reports ~3.5 bits per dimension for TurboQuant.
- **Cross-Layer Attention (CLA).** Adjacent layers share K/V state, halving KVCache — orthogonal to GQA/MLA.
- **MoE can amplify KVCache importance.** The survey reports workloads where KVCache reaches 60–80% of inference memory; the fraction depends on architecture, sequence length, batch shape, and runtime allocation.

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
