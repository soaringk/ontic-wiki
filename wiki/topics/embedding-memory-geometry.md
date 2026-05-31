# Embedding Memory Geometry

The geometric study of semantic memory systems: how embeddings are organized on the unit sphere, how their shape determines retrieval behavior under noise and compression, and how cluster geometry dictates the fundamental limits of consolidation and quantization.

## Core Ideas

- Embedding clusters live on the unit sphere `S^(d-1)` with two key geometric properties: mean within-cluster cosine distance `d̄` (spread) and effective dimension `d_eff` (participation ratio of the covariance spectrum).
- The Consolidation–Interference Duality proves that the same spectral quantity `(θ′/d̄)^(d_eff/2)` governs both forgetting under retrieval noise and identity loss under compression: compressing a cluster to fewer representatives does not escape the geometric trap.
- A tight/spread phase boundary exists at `d̄ = θ′`. Below it (tight regime), any consolidator preserves identity; above it (spread regime), identity loss is forced and grows with `d_eff`.
- Production sentence encoders concentrate ≥99% of variance in at most ~16 effective dimensions globally; local per-cluster `d_eff` is often below 5.
- On real text corpora (MS MARCO, Natural Questions, HotpotQA, Wikipedia, arXiv), clusters mostly sit in the tight regime, making simple centroid averaging near-optimal — adaptive routing buys nothing on real text.

## Sub-areas

- **Consolidation theory.** Lower bounds on identity-preserving compression for unit-norm embedding clusters; the Consolidation–Interference Duality and its cap-volume proof.
- **Effective dimension.** The participation ratio `(tr Σ)² / tr(Σ²)` as a scale-invariant, weighted measure of how many directions a cluster actually uses.
- **Geometry-Aware Consolidation (GAC).** A routing algorithm that selects centroid (tight regime) or residual-budgeted medoid (spread regime) based on local cluster geometry; used as a probe to show that adaptation does not beat centroid on real text.
- **Consolidation vs. quantization.** At matched bytes-per-vector, centroid consolidation dominates PQ/OPQ/LSH/PCA+int8/HNSW-prune on low-to-moderate-`d_eff` corpora; quantization wins only on high-`d_eff` arXiv titles.

## Related Concepts

- [Effective Dimension](../concepts/effective-dimension.md)

## Sources

- [The Geometry of Consolidation v6 (Paper)](../sources/geometry-of-consolidation-v6.md)
