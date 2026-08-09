---
kind: source
title: "The Geometry of Consolidation (NeurIPS 2026 submission)"
slug: geometry-of-consolidation-v6
source_ids:
  - raw-geometryofconsolidation-v6
  - raw-geometry-of-consolidation
status: active
raw_path: raw/GeometryOfConsolidation-v6.pdf
source_type: pdf
parser: mineru
published: 2026-04-19
created: 2026-05-26
updated: 2026-08-10
---

# Summary

This NeurIPS 2026 submission presents the Consolidation–Interference Duality: for any embedding cluster consolidated to fewer representatives, identity-retrieval error is lower-bounded by `1 - c₁·m·(θ′/d̄)^(d_eff/2)` where `d_eff` is the cluster's local effective dimension and `d̄` is its mean within-cluster cosine distance. The bound uses the same spectral quantity that the authors connect to forgetting under retrieval noise, hence "duality."

# Key Claims

- **The Consolidation–Interference Duality Theorem.** The manuscript proves that, under its unit-norm cosine-threshold retrieval assumptions, any consolidator mapping n cluster members to m < n representatives faces an identity-retrieval error floor set by `(θ′/d̄)^(d_eff/2)` when cap slack θ′ is smaller than within-cluster spread d̄.
- **Tight/spread phase boundary.** When `d̄ < θ′` (tight regime), every strategy achieves near-perfect identity preservation (cap-coverage error ≤ 0.5%). When `d̄ ≥ θ′` (spread regime), errors diverge to 30–74% in an order predicted by `d_eff`.
- **Centroid dominates on real text.** Across five real-text corpora (MS MARCO, Natural Questions, HotpotQA, Wikipedia sections, arXiv titles) and six sentence encoders, a fixed centroid picker beats a stochastic adaptive router (GAC) by 1–6 identity points. The residual-direction budget in the adaptive router contributes nearly nothing (Δ ≤ 0.002).
- **Geometry selects consolidation vs. quantization.** At matched bytes-per-vector, centroid consolidation dominates product quantization on low-to-moderate-`d_eff` corpora; quantization takes over only on high-`d_eff` arXiv titles.
- **Downstream RAG is regime-dependent.** A Llama-3.1-70B-Instruct pipeline on Natural Questions, HotpotQA, and PopQA shows a regime-dependent three-way split: centroid hurts NQ by 4.2 EM, is neutral on HotpotQA, and wins by 8.4 EM on PopQA — matching the cap-coverage prediction.

# Why It Matters

This is the third manuscript in a trilogy on the geometry of embedding memory. It argues that compression does not escape the same effective-dimension limits that the authors associate with forgetting under noise. Its finding that simple centroid averaging is near-optimal in the evaluated real-text setup motivates further RAG-system validation rather than a workload-general rule.

# Companion Repository Notes

The GitHub README captured at `raw/geometry-of-consolidation.md` points to the same work and adds practical reproduction context: the `gac/` package implements Geometry-Aware Consolidation, `results/` stores the experimental Parquet outputs, `scripts/make_figures.py` regenerates figures, and `scripts/calibrate_c1.py` reconstructs the bound calibration table. Its seven-corpus count and claim that GAC dominates the centroid conflict with the v6 PDF's six-corpus setup and finding that centroid wins on the five real-text corpora. The v6 PDF is therefore canonical here for scientific claims; the README is retained only as companion repository context.

# Connections

- Topic: [Embedding Memory Geometry](../topics/embedding-memory-geometry.md)
- Concept: [Effective Dimension](../concepts/effective-dimension.md)

# Open Questions

- The isotropic cap-volume bound is loose in the spread regime; an anisotropic refinement is the central open theoretical problem.
- Whether the law extends to multimodal embeddings, non-contrastive spaces, or biological memory is untested.
- The theorem applies to unit-norm embedding clusters under cosine-threshold retrieval — extensions to learned-state memory or raw LLM hidden states are open.
