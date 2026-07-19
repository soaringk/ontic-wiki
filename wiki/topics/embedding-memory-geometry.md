# Embedding Memory Geometry

The geometric study of semantic memory systems: how embeddings are organized on the unit sphere, how their shape determines retrieval behavior under noise and compression, and how cluster geometry dictates the fundamental limits of consolidation and quantization.

## Core Ideas

- Embedding clusters live on the unit sphere `S^(d-1)` with two key geometric properties: mean within-cluster cosine distance `d̄` (spread) and effective dimension `d_eff` (participation ratio of the covariance spectrum).
- The Consolidation–Interference Duality proves that the same spectral quantity `(θ′/d̄)^(d_eff/2)` governs both forgetting under retrieval noise and identity loss under compression: compressing a cluster to fewer representatives does not escape the geometric trap ([paper](../sources/geometry-of-consolidation-v6.md)).
- A tight/spread boundary is evaluated at `d̄ = θ′`. In the paper's tight-regime cases, the tested strategies achieve near-perfect identity preservation; in the spread regime, observed error rises with `d_eff`.
- In the paper's six evaluated sentence encoders, at least 99% of variance is concentrated in at most about 16 effective dimensions globally, and local per-cluster `d_eff` is often below 5.
- Across the paper's five evaluated text corpora and identity-retrieval setup, clusters mostly sit in the tight regime and centroid averaging matches or beats its tested adaptive router. This does not establish that adaptive routing is ineffective for all text workloads.

## Sub-areas

- **Consolidation theory.** Lower bounds on identity-preserving compression for unit-norm embedding clusters; the Consolidation–Interference Duality and its cap-volume proof.
- **Effective dimension.** The participation ratio `(tr Σ)² / tr(Σ²)` as a scale-invariant, weighted measure of how many directions a cluster actually uses.
- **Geometry-Aware Consolidation (GAC).** A routing algorithm that selects centroid (tight regime) or residual-budgeted medoid (spread regime) based on local cluster geometry; used as a probe showing that adaptation did not beat centroid on the five evaluated text corpora.
- **Consolidation vs. quantization.** In the paper's matched-bytes experiments, centroid consolidation beats the tested PQ/OPQ/LSH/PCA+int8/HNSW-prune configurations on its low-to-moderate-`d_eff` corpora; quantization wins on the evaluated high-`d_eff` arXiv-title corpus ([paper](../sources/geometry-of-consolidation-v6.md)).

## Related Concepts

- [Effective Dimension](../concepts/effective-dimension.md)

## Sources

- [The Geometry of Consolidation v6 (Paper)](../sources/geometry-of-consolidation-v6.md)
