---
kind: source
title: "The Geometry of Consolidation (NeurIPS 2026)"
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
updated: 2026-05-26
---

# Summary

This NeurIPS 2026 paper proves the Consolidation–Interference Duality: for any embedding cluster consolidated to fewer representatives, identity-retrieval error is lower-bounded by `1 - c₁·m·(θ′/d̄)^(d_eff/2)` where `d_eff` is the cluster's local effective dimension and `d̄` is its mean within-cluster cosine distance. The bound is the same spectral quantity that governs forgetting under retrieval noise — hence "duality."

# Key Claims

- **The Consolidation–Interference Duality Theorem.** Any consolidator mapping n unit-norm cluster members to m < n representatives faces an identity-retrieval error floor set by `(θ′/d̄)^(d_eff/2)` when the cap slack θ′ is smaller than the within-cluster spread d̄. The bound is provable, universal, and independent of the choice of consolidator.
- **Tight/spread phase boundary.** When `d̄ < θ′` (tight regime), every strategy achieves near-perfect identity preservation (cap-coverage error ≤ 0.5%). When `d̄ ≥ θ′` (spread regime), errors diverge to 30–74% in an order predicted by `d_eff`.
- **Centroid dominates on real text.** Across five real-text corpora (MS MARCO, Natural Questions, HotpotQA, Wikipedia sections, arXiv titles) and six sentence encoders, a fixed centroid picker beats a stochastic adaptive router (GAC) by 1–6 identity points. The residual-direction budget in the adaptive router contributes nearly nothing (Δ ≤ 0.002).
- **Geometry selects consolidation vs. quantization.** At matched bytes-per-vector, centroid consolidation dominates product quantization on low-to-moderate-`d_eff` corpora; quantization takes over only on high-`d_eff` arXiv titles.
- **Downstream RAG is regime-dependent.** A Llama-3.1-70B-Instruct pipeline on Natural Questions, HotpotQA, and PopQA shows a regime-dependent three-way split: centroid hurts NQ by 4.2 EM, is neutral on HotpotQA, and wins by 8.4 EM on PopQA — matching the cap-coverage prediction.

# Why It Matters

This is the third paper in a trilogy on the geometry of embedding memory. It closes the argument that compression does not provide an escape from the information-theoretic limits of semantic memory — the same effective dimension that governs forgetting under noise governs consolidation under compression. The practical finding that simple centroid averaging is near-optimal on real text has direct implications for RAG system design.

# Companion Repository Notes

The GitHub README captured at `raw/geometry-of-consolidation.md` points to the same work and adds practical reproduction context: the `gac/` package implements Geometry-Aware Consolidation, `results/` stores the experimental Parquet outputs, `scripts/make_figures.py` regenerates figures, and `scripts/calibrate_c1.py` reconstructs the bound calibration table. These repository details are kept here rather than in a duplicate source page because the README is a companion artifact for the same paper.

# Connections

- Topic: [Embedding Memory Geometry](../topics/embedding-memory-geometry.md)
- Concept: [Effective Dimension](../concepts/effective-dimension.md)

# Open Questions

- The isotropic cap-volume bound is loose in the spread regime; an anisotropic refinement is the central open theoretical problem.
- Whether the law extends to multimodal embeddings, non-contrastive spaces, or biological memory is untested.
- The theorem applies to unit-norm embedding clusters under cosine-threshold retrieval — extensions to learned-state memory or raw LLM hidden states are open.
